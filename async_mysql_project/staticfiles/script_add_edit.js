// // function formatDate(input) {
// //     let value = input.value.replace(/\D/g, '');  // Убираем все нецифровые символы
// //     if (value.length >= 5) {
// //         input.value = value.substring(0, 2) + '.' + value.substring(2, 4) + (value.length > 4 ? '.' + value.substring(4, 8) : '');
// //     } else if (value.length >= 3) {
// //         input.value = value.substring(0, 2) + '.' + value.substring(2, 4);
// //     } else {
// //         input.value = value;
// //     }
// // }

// function formatDate(input, event) {
//     const originalCursorPos = input.selectionStart;
//     let digits = input.value.replace(/\D/g, '').slice(0, 8);

//     // Форматируем строку как DD.MM.YYYY
//     let formatted = '';
//     for (let i = 0; i < digits.length; i++) {
//       if (i === 2 || i === 4) formatted += '.';
//       formatted += digits[i];
//     }

//     input.value = formatted;

//     // Управление позицией курсора
//     let cursorPos = originalCursorPos;

//     if (event.inputType !== 'deleteContentBackward') {
//       if (cursorPos === 3 || cursorPos === 6) cursorPos++;
//     }
//     input.setSelectionRange(cursorPos, cursorPos);

//     validateDate(input);
//   }

//   function validateDate(input) {
//     if (input.value.length !== 10) {
//       clearValidation(input);
//       return;
//     }

//     const [day, month, year] = input.value.split('.').map(Number);

//     const isValidYear = year >= 1900 && year <= 2100;
//     const isValidMonth = month >= 1 && month <= 12;
//     const maxDay = isValidYear && isValidMonth ? new Date(year, month, 0).getDate() : 31;
//     const isValidDay = day >= 1 && day <= maxDay;

//     if (isValidYear && isValidMonth && isValidDay) {
//       clearValidation(input);
//     } else {
//       setInvalid(input);
//     }
//   }

//   function setInvalid(input) {
//     input.style.borderColor = 'red';
//     input.setCustomValidity('Некорректная дата');
//   }

//   function clearValidation(input) {
//     input.style.borderColor = '';
//     input.setCustomValidity('');
//   }

// //   document.getElementById('dateInput').addEventListener('input', function(event) {
// //     formatDate(this, event);
// //   });

// //   document.getElementById('myForm').addEventListener('submit', function(e) {
// //     const input = document.getElementById('dateInput');
// //     if (!input.checkValidity()) {
// //       e.preventDefault();
// //       input.reportValidity();
// //     }
// //   });

// const MAX_VALUE = 10_000_000_000;

// function formatInputValue(val) {
//     val = val.replace(',', '.');               // Заменяем запятую на точку
//     val = val.replace(/[^0-9.]/g, '');         // Оставляем только цифры и точки

//     let parts = val.split('.');
//     if (parts.length > 2) {
//         val = parts[0] + '.' + parts.slice(1).join('');
//         parts = val.split('.');
//     }

//     if (parts[1]?.length > 2) {
//         parts[1] = parts[1].slice(0, 2);
//         val = parts.join('.');
//     }

//     let num = parseFloat(val);
//     if (!isNaN(num) && num > MAX_VALUE) {
//         val = MAX_VALUE.toString();
//     }

//     return val;
// }

// function formatOnBlur(val) {
//     if (val === '' || val === '.') return '0.00';

//     let num = parseFloat(val);
//     if (isNaN(num)) return '0.00';

//     if (num > MAX_VALUE) num = MAX_VALUE;

//     return num.toFixed(2);
// }

// function initializeEmptyFields() {
//     document.querySelectorAll('.num-field').forEach(input => {
//         if (input.value.trim() === '' || input.value.trim() === '.') {
//             input.value = '0.00';
//         } else {
//             // Приводим сразу к корректному формату
//             input.value = formatOnBlur(input.value);
//         }
//     });
// }

// document.addEventListener('input', (e) => {
//     if (e.target.classList.contains('num-field')) {
//         e.target.value = formatInputValue(e.target.value);
//     }
// });

// document.addEventListener('blur', (e) => {
//     if (e.target.classList.contains('num-field')) {
//         e.target.value = formatOnBlur(e.target.value);
//     }
// }, true);

// document.addEventListener('DOMContentLoaded', () => {
//     console.log("Старт script_add_edit.js");

//     const dateInput = document.getElementById('dateInput');
//     if (dateInput) {
//         dateInput.addEventListener('input', function(event) {
//             formatDate(this, event);
//         });
//     }

//     const myForm = document.getElementById('myForm');
//     if (myForm) {
//         myForm.addEventListener('submit', function(e) {
//             if (!dateInput.checkValidity()) {
//                 e.preventDefault();
//                 dateInput.reportValidity();
//             }
//         });
//     }

//     checkMandatoryFields();
//     initializeEmptyFields();

//     // Читаем scroll_position из текущего URL
//     const urlParams = new URLSearchParams(window.location.search);
//     const scrollPos = urlParams.get('scroll_position') || 0;

//     // 1. Для кнопки "Внести изменения" — добавляем в скрытое поле формы
//     document.getElementById('scroll_position_input').value = scrollPos;

//     // 2. Для кнопки "Вернуться назад" — добавляем в href
//     const backLink = document.getElementById('backLink');
//     if (backLink) {
//         const url = new URL(backLink.href, window.location.origin);
//         url.searchParams.set('scroll_position', scrollPos);
//         backLink.href = url.toString();
//     }

// });

// function checkMandatoryFields() {
//     // Функция для безопасного получения value
//     function safeValue(id) {
//         const el = document.getElementById(id);
//         return el ? el.value : null;
//     }

//     const statusSelect = document.getElementById('status');
//     const selectedStatus = safeValue('status');

//     const statusWay = document.getElementById('way');
//     const selectedStatusWay = safeValue('way');

//     const statusKTSSR = document.getElementById('KTSSR');
//     const selectedStatusKTSSR = safeValue('KTSSR');

//     const statusDopFC = document.getElementById('DopFC');
//     const selectedStatusDopFC = safeValue('DopFC');

//     const statusKOSGU = document.getElementById('KOSGU');
//     const selectedStatusKOSGU = safeValue('KOSGU');

//     // Потом достаём нужные поля
//     const statusesList = statuses.list || [];
//     const statusesBlocking = statuses.blocking || [];
//     const statusesMandatory = statuses.mandatory || [];
//     const statusesPurchasing_method = statuses.purchasing_method || [];
//     const statusesKTSSR = statuses.KTSSR || [];
//     const statusesDopFC = statuses.DopFC || [];
//     const statusesKOSGU = statuses.KOSGU || [];

//     const currentStatus = selectedStatus || "{{ status }}";
//     const currentWay = selectedStatusWay || "{{ way }}";
//     const currentKTSSR = selectedStatusKTSSR || "{{ KTSSR }}";
//     const currentDopFC = selectedStatusDopFC || "{{ DopFC }}";
//     const currentKOSGU = selectedStatusKOSGU || "{{ KOSGU }}";

//     // Для каждого элемента — обновляем, если он существует
//     if (statusWay) updateStatusSelect(statusWay, statusesPurchasing_method, currentWay);
//     if (statusSelect) updateStatusSelect(statusSelect, statusesList, currentStatus);
//     if (statusKTSSR) updateStatusSelect(statusKTSSR, statusesKTSSR, currentKTSSR);
//     if (statusDopFC) updateStatusSelect(statusDopFC, statusesDopFC, currentDopFC);
//     if (statusKOSGU) updateStatusSelect(statusKOSGU, statusesKOSGU, currentKOSGU);

//     updateMandatoryFields(currentStatus, statusesMandatory);
//     updateBlockingFields(currentStatus, statusesBlocking);

//     console.log("Завершение script_add_edit.js");
// }

// function updateStatusSelect(selectElement, statuses, currentStatus) {
//     selectElement.innerHTML = '';

//     const defaultOption = document.createElement('option');
//     defaultOption.value = '';
//     defaultOption.textContent = 'Выберите статус';
//     if (currentStatus === '') defaultOption.selected = true;
//     selectElement.appendChild(defaultOption);

//     statuses.forEach(status => {
//         const option = document.createElement('option');
//         option.value = status;
//         option.textContent = status;
//         if (status === currentStatus) option.selected = true;
//         selectElement.appendChild(option);
//     });
// }

// function updateMandatoryFields(status, statusesMandatory) {
//     const isMandatory = statusesMandatory.includes(status);
//     const mandatoryFields = ['counterparty', 'contract_number', 'contract_date', 'end_date'];

//     mandatoryFields.forEach(fieldId => {
//         const field = document.getElementById(fieldId);
//         if (!field) return;

//         if (isMandatory) {
//             field.setAttribute('required', 'required');
//         } else {
//             field.removeAttribute('required');
//         }
//     });
// }

// function updateBlockingFields(status, statusesBlocking) {
//     const isBlocked = statusesBlocking.includes(status);

//     const fieldsToBlock = [
//         'date_january_one', 'sum_january_one',
//         'date_february', 'sum_february',
//         'date_march', 'sum_march',
//         'date_april', 'sum_april',
//         'date_may', 'sum_may',
//         'date_june', 'sum_june',
//         'date_july', 'sum_july',
//         'date_august', 'sum_august',
//         'date_september', 'sum_september',
//         'date_october', 'sum_october',
//         'date_november', 'sum_november',
//         'date_december', 'sum_december',
//         'date_january_two', 'sum_january_two'
//     ];

//     fieldsToBlock.forEach(fieldId => {
//         const field = document.getElementById(fieldId);
//         if (!field) return;

//         if (isBlocked) {
//             field.setAttribute('readonly', true);
//             field.style.backgroundColor = '#f0f0f0';
//             field.value = '';
//         } else {
//             field.removeAttribute('readonly');
//             field.style.backgroundColor = '';
//         }
//     });
// }

// // document.addEventListener('DOMContentLoaded', function () {
// //     // Читаем scroll_position из текущего URL
// //     const urlParams = new URLSearchParams(window.location.search);
// //     const scrollPos = urlParams.get('scroll_position') || 0;

// //     // 1. Для кнопки "Внести изменения" — добавляем в скрытое поле формы
// //     document.getElementById('scroll_position_input').value = scrollPos;

// //     // 2. Для кнопки "Вернуться назад" — добавляем в href
// //     const backLink = document.getElementById('backLink');
// //     if (backLink) {
// //         const url = new URL(backLink.href, window.location.origin);
// //         url.searchParams.set('scroll_position', scrollPos);
// //         backLink.href = url.toString();
// //     }
// // });

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
    if (input.value.length !== 10) {
        clearValidation(input);
        return;
    }

    const [day, month, year] = input.value.split('.').map(Number);
    const isValidYear = year >= 1900 && year <= 2100;
    const isValidMonth = month >= 1 && month <= 12;
    const maxDay = isValidYear && isValidMonth ? new Date(year, month, 0).getDate() : 31;
    const isValidDay = day >= 1 && day <= maxDay;

    (isValidYear && isValidMonth && isValidDay) ? clearValidation(input) : setInvalid(input);
}

function setInvalid(input) {
    input.style.borderColor = 'red';
    input.setCustomValidity('Некорректная дата');
}

function clearValidation(input) {
    input.style.borderColor = '';
    input.setCustomValidity('');
}

// ==================== Числа ====================
const MAX_VALUE = 10_000_000_000;

function formatInputValue(val) {
    val = val.replace(',', '.').replace(/[^0-9.]/g, '');
    const parts = val.split('.');
    if (parts.length > 2) val = parts[0] + '.' + parts.slice(1).join('');

    const [intPart, decPart] = val.split('.');
    const formattedDec = decPart?.slice(0, 2) || '';
    let num = parseFloat(intPart + (formattedDec ? '.' + formattedDec : ''));

    if (!isNaN(num) && num > MAX_VALUE) num = MAX_VALUE;

    return isNaN(num) ? '' : (intPart + (formattedDec ? '.' + formattedDec : ''));
}

function formatOnBlur(val) {
    let num = parseFloat(val);
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
    const defaultOption = new Option('Выберите статус', '', currentStatus === '');
    selectElement.appendChild(defaultOption);

    statuses.forEach(status => {
        const option = document.createElement('option');
        option.value = status;
        option.text = status;
        option.selected = (status === currentStatus);
        selectElement.appendChild(option);
    });
}

function updateMandatoryFields(status, statusesMandatory) {
    const isMandatory = statusesMandatory.includes(status);
    const mandatoryFields = ['counterparty', 'contract_number', 'contract_date', 'end_date'];

    mandatoryFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field) return;
        isMandatory ? field.setAttribute('required', 'required') : field.removeAttribute('required');
    });
}

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

    updateMandatoryFields(currentStatus, statuses.mandatory || []);
    updateBlockingFields(currentStatus, statuses.blocking || []);
}

// ==================== Инициализация событий ====================
document.addEventListener('DOMContentLoaded', () => {
    console.log("Старт script_add_edit.js");

    const dateInput = document.getElementById('dateInput');
    if (dateInput) dateInput.addEventListener('input', e => formatDate(e.target, e));

    const myForm = document.getElementById('myForm');
    if (myForm && dateInput) {
        myForm.addEventListener('submit', e => {
            if (!dateInput.checkValidity()) {
                e.preventDefault();
                dateInput.reportValidity();
            }
        });
    }

    checkMandatoryFields();
    initializeEmptyFields();

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
});

document.addEventListener('input', e => {
    if (e.target.classList.contains('num-field')) e.target.value = formatInputValue(e.target.value);
});

document.addEventListener('blur', e => {
    if (e.target.classList.contains('num-field')) e.target.value = formatOnBlur(e.target.value);
}, true);
