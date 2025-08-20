// ==================== Дата ====================
function formatDate(input, event) {
    const originalCursorPos = input.selectionStart;
    let digits = input.value.replace(/\D/g, '').slice(0, 8);

    let formatted = '';
    for (let i = 0; i < digits.length; i++) {
        if (i === 2 || i === 4) formatted += '.';
        formatted += digits[i];
    }

    input.value = formatted;

    let cursorPos = originalCursorPos;
    if (event.inputType !== 'deleteContentBackward' && (cursorPos === 3 || cursorPos === 6)) {
        cursorPos++;
    }
    input.setSelectionRange(cursorPos, cursorPos);

    validateDate(input);
}

function validateDate(input) {
    const [day, month, year] = input.value.split('.').map(Number);
    const isValidYear = year >= 1900 && year <= 2100;
    const isValidMonth = month >= 1 && month <= 12;
    const maxDay = isValidYear && isValidMonth ? new Date(year, month, 0).getDate() : 31;
    const isValidDay = day >= 1 && day <= maxDay;

    if (input.value.length !== 10 || !isValidYear || !isValidMonth || !isValidDay) {
        setInvalid(input, 'Некорректная дата');
        return false;
    } else {
        clearValidation(input);
        return true;
    }
}

// ==================== Вспомогательные функции ====================
function setInvalid(el, msg) {
    el.classList.add('invalid');
    el.setCustomValidity(msg || 'Ошибка');
    el.reportValidity();
}

function clearValidation(el) {
    el.classList.remove('invalid');
    el.setCustomValidity('');
}

// ==================== Числа ====================
const MAX_VALUE = 10_000_000_000;

function formatInputValue(val) {
    if (!val) return '';

    // Заменяем запятую на точку
    val = val.replace(',', '.');

    // Разрешаем временно вводить только точку
    if (val === '.') return '.';

    // Убираем все кроме цифр и точки
    val = val.replace(/[^0-9.]/g, '');

    // Разрешаем только одну точку
    const parts = val.split('.');
    if (parts.length > 2) val = parts[0] + '.' + parts.slice(1).join('');

    // Ограничиваем число десятичных знаков до 2
    const [intPart, decPart] = val.split('.');
    const formattedDec = decPart?.slice(0, 2) || '';

    // Ограничение максимального значения
    let num = parseFloat(intPart + (formattedDec ? '.' + formattedDec : ''));
    if (!isNaN(num) && num > MAX_VALUE) num = MAX_VALUE;

    // Если пользователь ввёл только точку после цифр — оставляем её
    if (val.endsWith('.') && !formattedDec) return intPart + '.';

    return intPart + (formattedDec ? '.' + formattedDec : '');
}

function prepareForSubmit(value) {
    return value
        .replace(/\s+/g, '')        // убрать пробелы
        .replace(/,/g, '.')         // заменить запятую на точку
        .replace(/[^0-9.]/g, '');   // убрать всё, кроме цифр и точки
}

function formatOnBlur(val) {
    let cleanStr = prepareForSubmit(val);  // сначала чистим строку
    let num = parseFloat(cleanStr);        // потом парсим в число
    if (isNaN(num) || val === '' || val === '.') return '0.00';
    if (num > MAX_VALUE) num = MAX_VALUE;
    return num.toFixed(2);
}

function initializeEmptyFields() {
    document.querySelectorAll('.num-field').forEach(input => {
        input.value = (input.value.trim() === '' || input.value.trim() === '.') ? '0.00' : formatOnBlur(input.value);
    });
}

// ==================== Статусы и обязательные поля ====================
function safeValue(id) {
    const el = document.getElementById(id);
    return el ? el.value : null;
}

function updateStatusSelect(selectElement, statuses, currentStatus) {
    selectElement.innerHTML = '';
    const defaultOption = new Option('Выберите', '', currentStatus === '');
    selectElement.appendChild(defaultOption);

    statuses.forEach(status => {
        const option = document.createElement('option');
        option.value = status;
        option.text = status;
        option.selected = (status === currentStatus);
        selectElement.appendChild(option);
    });
}

// function updateMandatoryFields(status, statusesMandatory) {
//     const isMandatory = statusesMandatory.includes(status);
//     const mandatoryFields = ['counterparty', 'contract_number', 'contract_date', 'end_date'];

//     // Проверка обязательных полей
//     mandatoryFields.forEach(fieldId => {
//         const field = document.getElementById(fieldId);
//         if (!field) return;

//         if (isMandatory) {
//             if (field.id.includes('date')) {
//                 // Для дат — проверка через validateDate
//                 if (!validateDate(field)) allValid = false;
//             } else {
//                 // Для текстовых/других полей
//                 if (!field.value.trim()) {
//                     setInvalid(field, 'Поле обязательно для заполнения');
//                     allValid = false;
//                 } else {
//                     clearValidation(field);
//                 }
//             }
//         } else {
//             clearValidation(field); // Снимаем ошибку, если поле не обязательно
//         }
//     });
// }

function updateBlockingFields(status, statusesBlocking) {
    const isBlocked = statusesBlocking.includes(status);
    const fieldsToBlock = [
        'date_january_one', 'sum_january_one', 'date_february', 'sum_february',
        'date_march', 'sum_march', 'date_april', 'sum_april', 'date_may', 'sum_may',
        'date_june', 'sum_june', 'date_july', 'sum_july', 'date_august', 'sum_august',
        'date_september', 'sum_september', 'date_october', 'sum_october', 'date_november', 'sum_november',
        'date_december', 'sum_december', 'date_january_two', 'sum_january_two'
    ];

    fieldsToBlock.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field) return;
        if (isBlocked) {
            field.setAttribute('readonly', true);
            field.style.backgroundColor = '#f0f0f0';
            field.value = '';
        } else {
            field.removeAttribute('readonly');
            field.style.backgroundColor = '';
        }
    });
}

function getCurrentFromDiv(divId, dataAttr) {
    const div = document.getElementById(divId);
    return div ? div.getAttribute(`data-${dataAttr}`) || '' : '';
}

function checkMandatoryFields() {
    const currentStatus = safeValue('status') || getCurrentFromDiv('status-container', 'current-status');
    const currentWay = safeValue('way') || getCurrentFromDiv('way-container', 'current-way');
    const currentKTSSR = safeValue('KTSSR') || getCurrentFromDiv('KTSSR-container', 'current-KTSSR');
    const currentDopFC = safeValue('DopFC') || getCurrentFromDiv('DopFC-container', 'current-DopFC');
    const currentKOSGU = safeValue('KOSGU') || getCurrentFromDiv('KOSGU-container', 'current-KOSGU');

    if (document.getElementById('status')) updateStatusSelect(document.getElementById('status'), statuses.list || [], currentStatus);
    if (document.getElementById('way')) updateStatusSelect(document.getElementById('way'), statuses.purchasing_method || [], currentWay);
    if (document.getElementById('KTSSR')) updateStatusSelect(document.getElementById('KTSSR'), statuses.KTSSR || [], currentKTSSR);
    if (document.getElementById('DopFC')) updateStatusSelect(document.getElementById('DopFC'), statuses.DopFC || [], currentDopFC);
    if (document.getElementById('KOSGU')) updateStatusSelect(document.getElementById('KOSGU'), statuses.KOSGU || [], currentKOSGU);

    // updateMandatoryFields(currentStatus, statuses.mandatory || []);
    validateForm();
    updateBlockingFields(currentStatus, statuses.blocking || []);
}

function validateForm() {
    let allValid = true;

    const fieldsToCheck = [
        { id: 'id_id', msg: 'Выберите номер закупки' },
        { id: 'name', msg: 'Выберите Наименование закупки' },
        { id: 'NMCC', msg: 'Выберите НМЦК' },
        { id: 'KTSSR', msg: 'Выберите КЦСР' },
        { id: 'KOSGU', msg: 'Выберите КОСГУ' },
        { id: 'DopFC', msg: 'Выберите ДопФК' },
    ];

    // Проверка основных полей
    fieldsToCheck.forEach(({ id, msg }) => {
        const el = document.getElementById(id);
        if (!el) return;

        if (el.type === 'text' && id.includes('date')) {
            if (!validateDate(el)) allValid = false;
        } else if (!el.value) {
            setInvalid(el, msg);
            allValid = false;
        } else {
            clearValidation(el);
        }
    });

    // Получаем статус
    const status = safeValue('status') || getCurrentFromDiv('status-container', 'current-status');

    // Безопасно получаем список обязательных статусов
    const statusesMandatory = (typeof statuses !== 'undefined' && Array.isArray(statuses.mandatory))
        ? statuses.mandatory
        : [];

    const isMandatory = statusesMandatory.includes(status);
    const mandatoryFields = ['counterparty', 'contract_number', 'contract_date', 'end_date'];

    // Проверка обязательных полей по статусу
    mandatoryFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field) return;

        if (isMandatory) {
            if (fieldId.includes('date')) {
                if (!validateDate(field)) allValid = false;
            } else if (!field.value.trim()) {
                setInvalid(field, 'Поле обязательно для заполнения');
                allValid = false;
            } else {
                clearValidation(field);
            }
        } else {
            clearValidation(field);
        }
    });

    return allValid;
}

// Общая функция для проверки select
function validateSelectField(el, msg) {
    if (!el.value) {
        setInvalid(el, msg);
    } else {
        clearValidation(el);
    }
}

document.addEventListener('change', e => {
    // Блок для KTSSR, KOSGU, DopFC
    if (['KTSSR', 'KOSGU', 'DopFC'].includes(e.target.id)) {
        const msg = e.target.id === 'KTSSR' ? 'Выберите КЦСР' :
            e.target.id === 'KOSGU' ? 'Выберите КОСГУ' :
                'Выберите ДопФК';
        validateSelectField(e.target, msg);
    }

    // Блок для id_id, name, NMCC
    if (['id_id', 'name', 'NMCC'].includes(e.target.id)) {
        const msg = e.target.id === 'id_id' ? 'Выберите номер закупки' :
            e.target.id === 'name' ? 'Выберите Наименование закупки' :
                'Выберите НМЦК';
        validateSelectField(e.target, msg);
    }

    // Блок для counterparty, contract_number, contract_date, end_date
    if (['counterparty', 'contract_number', 'contract_date', 'end_date'].includes(e.target.id)) {
        // Получаем статус
        const status = safeValue('status') || getCurrentFromDiv('status-container', 'current-status');

        // Безопасно получаем список обязательных статусов
        const statusesMandatory = (typeof statuses !== 'undefined' && Array.isArray(statuses.mandatory))
            ? statuses.mandatory
            : [];

        const isMandatory = statusesMandatory.includes(status);
        const mandatoryFields = ['counterparty', 'contract_number', 'contract_date', 'end_date'];

        // Проверяем условие
        if (isMandatory && mandatoryFields.includes(e.target.id)) {
            const msg = e.target.id === 'counterparty' ? 'Выберите контрагента' :
                e.target.id === 'contract_number' ? 'Укажите номер договора' :
                    e.target.id === 'contract_date' ? 'Выберите дату договора' :
                        'Выберите дату окончания договора';
            validateSelectField(e.target, msg);
        }
    }
});

// Ограничение ввода только чисел для id_id (если элемент существует)
const idInput = document.getElementById('id_id');
if (idInput) {
    idInput.addEventListener('input', function () {
        this.value = this.value.replace(/\D/g, '');
    });
}

// ==================== Инициализация событий ====================
document.addEventListener('DOMContentLoaded', () => {
    console.log("Старт script_add_edit.js");

    if (typeof statuses !== 'undefined') {
        checkMandatoryFields();
    }
    initializeEmptyFields();

    // Validate the form immediately on page load
    validateForm(); // Add this line to trigger validation on page load

    // Работа с scroll_position
    const scrollPos = new URLSearchParams(window.location.search).get('scroll_position') || 0;
    const scrollInput = document.getElementById('scroll_position_input');
    if (scrollInput) scrollInput.value = scrollPos;

    const backLink = document.getElementById('backLink');
    if (backLink) {
        const url = new URL(backLink.href, window.location.origin);
        url.searchParams.set('scroll_position', scrollPos);
        backLink.href = url.toString();
    }

    document.addEventListener('input', e => {
        if (e.target.classList.contains('num-field')) e.target.value = formatInputValue(e.target.value);
    });

    document.addEventListener('blur', e => {
        if (e.target.classList.contains('num-field')) e.target.value = formatOnBlur(e.target.value);
    }, true);

});