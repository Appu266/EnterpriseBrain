CREATE OR REPLACE PACKAGE employee_operations_pkg AS

    /*
      Package Name : EMPLOYEE_OPERATIONS_PKG
      Purpose      : Manage employee creation, updates, termination,
                     salary calculations, bonus processing and audit logging.
    */

    TYPE employee_summary_rec IS RECORD (
        employee_id      NUMBER,
        employee_name    VARCHAR2(200),
        department_name  VARCHAR2(100),
        employment_status VARCHAR2(30),
        annual_salary    NUMBER,
        manager_name     VARCHAR2(200)
    );

    TYPE employee_summary_tab IS TABLE OF employee_summary_rec;

    PROCEDURE create_employee (
        p_first_name       IN VARCHAR2,
        p_last_name        IN VARCHAR2,
        p_email            IN VARCHAR2,
        p_department_id    IN NUMBER,
        p_manager_id       IN NUMBER,
        p_joining_date     IN DATE,
        p_monthly_salary   IN NUMBER,
        p_created_by       IN VARCHAR2,
        p_employee_id      OUT NUMBER
    );

    PROCEDURE update_employee_salary (
        p_employee_id      IN NUMBER,
        p_new_salary       IN NUMBER,
        p_effective_date   IN DATE,
        p_updated_by       IN VARCHAR2
    );

    PROCEDURE transfer_employee (
        p_employee_id        IN NUMBER,
        p_new_department_id  IN NUMBER,
        p_new_manager_id     IN NUMBER,
        p_transfer_date      IN DATE,
        p_updated_by         IN VARCHAR2
    );

    PROCEDURE terminate_employee (
        p_employee_id       IN NUMBER,
        p_termination_date  IN DATE,
        p_reason            IN VARCHAR2,
        p_updated_by        IN VARCHAR2
    );

    PROCEDURE process_department_bonus (
        p_department_id  IN NUMBER,
        p_bonus_percent  IN NUMBER,
        p_processed_by   IN VARCHAR2
    );

    FUNCTION calculate_annual_salary (
        p_employee_id IN NUMBER
    ) RETURN NUMBER;

    FUNCTION calculate_bonus (
        p_employee_id   IN NUMBER,
        p_bonus_percent IN NUMBER
    ) RETURN NUMBER;

    FUNCTION get_employee_summary (
        p_employee_id IN NUMBER
    ) RETURN employee_summary_rec;

    FUNCTION get_department_employees (
        p_department_id IN NUMBER
    ) RETURN employee_summary_tab PIPELINED;

END employee_operations_pkg;
/

CREATE OR REPLACE PACKAGE BODY employee_operations_pkg AS

    c_active_status     CONSTANT VARCHAR2(30) := 'ACTIVE';
    c_inactive_status   CONSTANT VARCHAR2(30) := 'INACTIVE';
    c_max_bonus_percent CONSTANT NUMBER := 25;

    e_invalid_salary     EXCEPTION;
    e_invalid_bonus      EXCEPTION;
    e_employee_not_found EXCEPTION;
    e_invalid_department EXCEPTION;

    PRAGMA EXCEPTION_INIT(e_employee_not_found, -20001);
    PRAGMA EXCEPTION_INIT(e_invalid_department, -20002);

    PROCEDURE write_audit_log (
        p_employee_id  IN NUMBER,
        p_action       IN VARCHAR2,
        p_old_value    IN VARCHAR2,
        p_new_value    IN VARCHAR2,
        p_performed_by IN VARCHAR2
    ) IS
    BEGIN
        INSERT INTO employee_audit_log (
            audit_id,
            employee_id,
            action_name,
            old_value,
            new_value,
            performed_by,
            performed_at
        )
        VALUES (
            employee_audit_seq.NEXTVAL,
            p_employee_id,
            p_action,
            p_old_value,
            p_new_value,
            p_performed_by,
            SYSDATE
        );
    END write_audit_log;

    PROCEDURE validate_department (
        p_department_id IN NUMBER
    ) IS
        l_department_count NUMBER;
    BEGIN
        SELECT COUNT(*)
          INTO l_department_count
          FROM departments
         WHERE department_id = p_department_id
           AND status = 'ACTIVE';

        IF l_department_count = 0 THEN
            RAISE_APPLICATION_ERROR(
                -20002,
                'Department does not exist or is inactive.'
            );
        END IF;
    END validate_department;

    FUNCTION employee_exists (
        p_employee_id IN NUMBER
    ) RETURN BOOLEAN IS
        l_employee_count NUMBER;
    BEGIN
        SELECT COUNT(*)
          INTO l_employee_count
          FROM employees
         WHERE employee_id = p_employee_id;

        RETURN l_employee_count > 0;
    END employee_exists;

    PROCEDURE create_employee (
        p_first_name       IN VARCHAR2,
        p_last_name        IN VARCHAR2,
        p_email            IN VARCHAR2,
        p_department_id    IN NUMBER,
        p_manager_id       IN NUMBER,
        p_joining_date     IN DATE,
        p_monthly_salary   IN NUMBER,
        p_created_by       IN VARCHAR2,
        p_employee_id      OUT NUMBER
    ) IS
        l_email_count NUMBER;
    BEGIN
        IF p_monthly_salary <= 0 THEN
            RAISE e_invalid_salary;
        END IF;

        validate_department(p_department_id);

        SELECT COUNT(*)
          INTO l_email_count
          FROM employees
         WHERE UPPER(email) = UPPER(p_email);

        IF l_email_count > 0 THEN
            RAISE_APPLICATION_ERROR(
                -20003,
                'An employee already exists with the supplied email address.'
            );
        END IF;

        p_employee_id := employee_seq.NEXTVAL;

        INSERT INTO employees (
            employee_id,
            first_name,
            last_name,
            email,
            department_id,
            manager_id,
            joining_date,
            monthly_salary,
            employment_status,
            created_by,
            created_at
        )
        VALUES (
            p_employee_id,
            TRIM(p_first_name),
            TRIM(p_last_name),
            LOWER(TRIM(p_email)),
            p_department_id,
            p_manager_id,
            NVL(p_joining_date, SYSDATE),
            p_monthly_salary,
            c_active_status,
            p_created_by,
            SYSDATE
        );

        write_audit_log(
            p_employee_id  => p_employee_id,
            p_action       => 'CREATE_EMPLOYEE',
            p_old_value    => NULL,
            p_new_value    => 'Employee created with salary ' ||
                              TO_CHAR(p_monthly_salary),
            p_performed_by => p_created_by
        );

        COMMIT;

    EXCEPTION
        WHEN e_invalid_salary THEN
            ROLLBACK;
            RAISE_APPLICATION_ERROR(
                -20004,
                'Monthly salary must be greater than zero.'
            );

        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END create_employee;

    PROCEDURE update_employee_salary (
        p_employee_id      IN NUMBER,
        p_new_salary       IN NUMBER,
        p_effective_date   IN DATE,
        p_updated_by       IN VARCHAR2
    ) IS
        l_old_salary employees.monthly_salary%TYPE;
    BEGIN
        IF p_new_salary <= 0 THEN
            RAISE e_invalid_salary;
        END IF;

        SELECT monthly_salary
          INTO l_old_salary
          FROM employees
         WHERE employee_id = p_employee_id
           AND employment_status = c_active_status
         FOR UPDATE;

        INSERT INTO employee_salary_history (
            salary_history_id,
            employee_id,
            old_salary,
            new_salary,
            effective_date,
            changed_by,
            changed_at
        )
        VALUES (
            employee_salary_history_seq.NEXTVAL,
            p_employee_id,
            l_old_salary,
            p_new_salary,
            NVL(p_effective_date, SYSDATE),
            p_updated_by,
            SYSDATE
        );

        UPDATE employees
           SET monthly_salary = p_new_salary,
               updated_by = p_updated_by,
               updated_at = SYSDATE
         WHERE employee_id = p_employee_id;

        write_audit_log(
            p_employee_id  => p_employee_id,
            p_action       => 'UPDATE_SALARY',
            p_old_value    => TO_CHAR(l_old_salary),
            p_new_value    => TO_CHAR(p_new_salary),
            p_performed_by => p_updated_by
        );

        COMMIT;

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            ROLLBACK;
            RAISE_APPLICATION_ERROR(
                -20001,
                'Active employee was not found.'
            );

        WHEN e_invalid_salary THEN
            ROLLBACK;
            RAISE_APPLICATION_ERROR(
                -20004,
                'New salary must be greater than zero.'
            );

        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END update_employee_salary;

    PROCEDURE transfer_employee (
        p_employee_id        IN NUMBER,
        p_new_department_id  IN NUMBER,
        p_new_manager_id     IN NUMBER,
        p_transfer_date      IN DATE,
        p_updated_by         IN VARCHAR2
    ) IS
        l_old_department_id employees.department_id%TYPE;
        l_old_manager_id    employees.manager_id%TYPE;
    BEGIN
        validate_department(p_new_department_id);

        SELECT department_id,
               manager_id
          INTO l_old_department_id,
               l_old_manager_id
          FROM employees
         WHERE employee_id = p_employee_id
           AND employment_status = c_active_status
         FOR UPDATE;

        UPDATE employees
           SET department_id = p_new_department_id,
               manager_id = p_new_manager_id,
               updated_by = p_updated_by,
               updated_at = SYSDATE
         WHERE employee_id = p_employee_id;

        INSERT INTO employee_transfer_history (
            transfer_id,
            employee_id,
            old_department_id,
            new_department_id,
            old_manager_id,
            new_manager_id,
            transfer_date,
            transferred_by
        )
        VALUES (
            employee_transfer_seq.NEXTVAL,
            p_employee_id,
            l_old_department_id,
            p_new_department_id,
            l_old_manager_id,
            p_new_manager_id,
            NVL(p_transfer_date, SYSDATE),
            p_updated_by
        );

        write_audit_log(
            p_employee_id  => p_employee_id,
            p_action       => 'TRANSFER_EMPLOYEE',
            p_old_value    => 'Department=' || l_old_department_id ||
                              ', Manager=' || l_old_manager_id,
            p_new_value    => 'Department=' || p_new_department_id ||
                              ', Manager=' || p_new_manager_id,
            p_performed_by => p_updated_by
        );

        COMMIT;

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            ROLLBACK;
            RAISE_APPLICATION_ERROR(
                -20001,
                'Active employee was not found.'
            );

        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END transfer_employee;

    PROCEDURE terminate_employee (
        p_employee_id       IN NUMBER,
        p_termination_date  IN DATE,
        p_reason            IN VARCHAR2,
        p_updated_by        IN VARCHAR2
    ) IS
        l_current_status employees.employment_status%TYPE;
    BEGIN
        SELECT employment_status
          INTO l_current_status
          FROM employees
         WHERE employee_id = p_employee_id
         FOR UPDATE;

        IF l_current_status = c_inactive_status THEN
            RAISE_APPLICATION_ERROR(
                -20005,
                'Employee is already inactive.'
            );
        END IF;

        UPDATE employees
           SET employment_status = c_inactive_status,
               termination_date = NVL(p_termination_date, SYSDATE),
               termination_reason = p_reason,
               updated_by = p_updated_by,
               updated_at = SYSDATE
         WHERE employee_id = p_employee_id;

        UPDATE user_accounts
           SET account_status = 'DISABLED',
               disabled_at = SYSDATE
         WHERE employee_id = p_employee_id;

        write_audit_log(
            p_employee_id  => p_employee_id,
            p_action       => 'TERMINATE_EMPLOYEE',
            p_old_value    => l_current_status,
            p_new_value    => c_inactive_status ||
                              ', Reason=' || p_reason,
            p_performed_by => p_updated_by
        );

        COMMIT;

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            ROLLBACK;
            RAISE_APPLICATION_ERROR(
                -20001,
                'Employee was not found.'
            );

        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END terminate_employee;

    FUNCTION calculate_annual_salary (
        p_employee_id IN NUMBER
    ) RETURN NUMBER IS
        l_monthly_salary employees.monthly_salary%TYPE;
    BEGIN
        SELECT monthly_salary
          INTO l_monthly_salary
          FROM employees
         WHERE employee_id = p_employee_id
           AND employment_status = c_active_status;

        RETURN l_monthly_salary * 12;

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(
                -20001,
                'Active employee was not found.'
            );
    END calculate_annual_salary;

    FUNCTION calculate_bonus (
        p_employee_id   IN NUMBER,
        p_bonus_percent IN NUMBER
    ) RETURN NUMBER IS
        l_annual_salary NUMBER;
    BEGIN
        IF p_bonus_percent <= 0
           OR p_bonus_percent > c_max_bonus_percent THEN
            RAISE e_invalid_bonus;
        END IF;

        l_annual_salary := calculate_annual_salary(
            p_employee_id
        );

        RETURN ROUND(
            l_annual_salary * p_bonus_percent / 100,
            2
        );

    EXCEPTION
        WHEN e_invalid_bonus THEN
            RAISE_APPLICATION_ERROR(
                -20006,
                'Bonus percentage must be between 0 and 25.'
            );
    END calculate_bonus;

    PROCEDURE process_department_bonus (
        p_department_id  IN NUMBER,
        p_bonus_percent  IN NUMBER,
        p_processed_by   IN VARCHAR2
    ) IS
        CURSOR c_employees IS
            SELECT employee_id
              FROM employees
             WHERE department_id = p_department_id
               AND employment_status = c_active_status
             FOR UPDATE SKIP LOCKED;

        l_bonus_amount NUMBER;
        l_processed_count NUMBER := 0;
    BEGIN
        validate_department(p_department_id);

        IF p_bonus_percent <= 0
           OR p_bonus_percent > c_max_bonus_percent THEN
            RAISE e_invalid_bonus;
        END IF;

        FOR employee_rec IN c_employees LOOP
            l_bonus_amount := calculate_bonus(
                employee_rec.employee_id,
                p_bonus_percent
            );

            INSERT INTO employee_bonus (
                bonus_id,
                employee_id,
                bonus_percent,
                bonus_amount,
                processed_by,
                processed_at
            )
            VALUES (
                employee_bonus_seq.NEXTVAL,
                employee_rec.employee_id,
                p_bonus_percent,
                l_bonus_amount,
                p_processed_by,
                SYSDATE
            );

            write_audit_log(
                p_employee_id  => employee_rec.employee_id,
                p_action       => 'PROCESS_BONUS',
                p_old_value    => NULL,
                p_new_value    => 'Bonus=' ||
                                  TO_CHAR(l_bonus_amount),
                p_performed_by => p_processed_by
            );

            l_processed_count := l_processed_count + 1;

            IF MOD(l_processed_count, 100) = 0 THEN
                COMMIT;
            END IF;
        END LOOP;

        COMMIT;

    EXCEPTION
        WHEN e_invalid_bonus THEN
            ROLLBACK;
            RAISE_APPLICATION_ERROR(
                -20006,
                'Bonus percentage must be between 0 and 25.'
            );

        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END process_department_bonus;

    FUNCTION get_employee_summary (
        p_employee_id IN NUMBER
    ) RETURN employee_summary_rec IS
        l_summary employee_summary_rec;
    BEGIN
        SELECT e.employee_id,
               e.first_name || ' ' || e.last_name,
               d.department_name,
               e.employment_status,
               e.monthly_salary * 12,
               m.first_name || ' ' || m.last_name
          INTO l_summary.employee_id,
               l_summary.employee_name,
               l_summary.department_name,
               l_summary.employment_status,
               l_summary.annual_salary,
               l_summary.manager_name
          FROM employees e
          JOIN departments d
            ON d.department_id = e.department_id
          LEFT JOIN employees m
            ON m.employee_id = e.manager_id
         WHERE e.employee_id = p_employee_id;

        RETURN l_summary;

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(
                -20001,
                'Employee was not found.'
            );
    END get_employee_summary;

    FUNCTION get_department_employees (
        p_department_id IN NUMBER
    ) RETURN employee_summary_tab PIPELINED IS
        l_summary employee_summary_rec;
    BEGIN
        validate_department(p_department_id);

        FOR employee_rec IN (
            SELECT e.employee_id,
                   e.first_name || ' ' || e.last_name employee_name,
                   d.department_name,
                   e.employment_status,
                   e.monthly_salary * 12 annual_salary,
                   m.first_name || ' ' || m.last_name manager_name
              FROM employees e
              JOIN departments d
                ON d.department_id = e.department_id
              LEFT JOIN employees m
                ON m.employee_id = e.manager_id
             WHERE e.department_id = p_department_id
             ORDER BY e.last_name,
                      e.first_name
        ) LOOP
            l_summary.employee_id := employee_rec.employee_id;
            l_summary.employee_name := employee_rec.employee_name;
            l_summary.department_name := employee_rec.department_name;
            l_summary.employment_status := employee_rec.employment_status;
            l_summary.annual_salary := employee_rec.annual_salary;
            l_summary.manager_name := employee_rec.manager_name;

            PIPE ROW(l_summary);
        END LOOP;

        RETURN;
    END get_department_employees;

END employee_operations_pkg;
/
