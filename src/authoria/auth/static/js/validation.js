function authDataValidation(auth_data) {
    var errors = []
    
    for (const [field, value] of Object.entries(auth_data)) {
        if (value.length === 0) {
            errors.push({'field': field, 'text': 'Заполните данное поле'});
            continue
        }
        
        if (field == 'username') {
            if (username_regex.test(value) == false) {
                errors.push({'field': field, 'text': 'Некорректное имя. Используйте: a-z 0-9 _'});
            }
        }

        else if (field == 'email') {
            if (email_regex.test(value) == false) {
                errors.push({'field': field, 'text': 'Некорректный E-Mail'});
            }
        }

        else if (field == 'username_or_email') {
            if (username_regex.test(value) == false && email_regex.test(value) == false) {
                errors.push({'field': field, 'text': 'Некорректное имя или e-mail'});
            }
        }

        else if (field == 'password') {
            if (value.length < 8) {
                errors.push({'field': field, 'text': 'Сликшом короткий пароль'});
            } 
            else if (password_regex.test(value) == false) {
                errors.push({'field': field, 'text': 'Некорректный пароль'});
            }
        }

        else if (field == 'password-confirm') {
            if (!(value === auth_data['password'])) {
                errors.push({'field': 'password', 'text': 'Пароли не совпадают'});
                errors.push({'field': 'password-confirm', 'text': 'Пароли не совпадают'});
            }
        }
    }

    return errors;
}