function formatDate(input) {
    let value = input.value.replace(/\D/g, '');  // Убираем все нецифровые символы
    if (value.length >= 5) {
        input.value = value.substring(0, 2) + '.' + value.substring(2, 4) + (value.length > 4 ? '.' + value.substring(4, 8) : '');
    } else if (value.length >= 3) {
        input.value = value.substring(0, 2) + '.' + value.substring(2, 4);
    } else {
        input.value = value;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    console.log("Старт script_add_edit.js");
    checkMandatoryFields(); // Вызов функции при загрузке страницы
});

// function checkMandatoryFields() {
//     const statusSelect = document.getElementById('status');
//     const selectedStatus = statusSelect.value;

//     const statusWay = document.getElementById('way');
//     const selectedStatusWay = statusWay.value;

//     const statusKTSSR = document.getElementById('KTSSR');
//     const selectedStatusKTSSR = statusKTSSR.value;

//     const statusDopFC = document.getElementById('DopFC');
//     const selectedStatusDopFC = statusDopFC.value;

//     const statusKOSGU = document.getElementById('KOSGU');
//     const selectedStatusKOSGU = statusKOSGU.value;

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

//     updateStatusSelect(statusWay, statusesPurchasing_method, currentWay);
//     updateStatusSelect(statusSelect, statusesList, currentStatus);
//     updateStatusSelect(statusKTSSR, statusesKTSSR, currentKTSSR);
//     updateStatusSelect(statusDopFC, statusesDopFC, currentDopFC);
//     updateStatusSelect(statusKOSGU, statusesKOSGU, currentKOSGU);
//     updateMandatoryFields(currentStatus, statusesMandatory);
//     updateBlockingFields(currentStatus, statusesBlocking);
//     console.log("Завершение script_add_edit.js");
// }

function checkMandatoryFields() {
    // Функция для безопасного получения value
    function safeValue(id) {
        const el = document.getElementById(id);
        return el ? el.value : null;
    }

    const statusSelect = document.getElementById('status');
    const selectedStatus = safeValue('status');

    const statusWay = document.getElementById('way');
    const selectedStatusWay = safeValue('way');

    const statusKTSSR = document.getElementById('KTSSR');
    const selectedStatusKTSSR = safeValue('KTSSR');

    const statusDopFC = document.getElementById('DopFC');
    const selectedStatusDopFC = safeValue('DopFC');

    const statusKOSGU = document.getElementById('KOSGU');
    const selectedStatusKOSGU = safeValue('KOSGU');

    // Потом достаём нужные поля
    const statusesList = statuses.list || [];
    const statusesBlocking = statuses.blocking || [];
    const statusesMandatory = statuses.mandatory || [];
    const statusesPurchasing_method = statuses.purchasing_method || [];
    const statusesKTSSR = statuses.KTSSR || [];
    const statusesDopFC = statuses.DopFC || [];
    const statusesKOSGU = statuses.KOSGU || [];

    const currentStatus = selectedStatus || "{{ status }}";
    const currentWay = selectedStatusWay || "{{ way }}";
    const currentKTSSR = selectedStatusKTSSR || "{{ KTSSR }}";
    const currentDopFC = selectedStatusDopFC || "{{ DopFC }}";
    const currentKOSGU = selectedStatusKOSGU || "{{ KOSGU }}";

    // Для каждого элемента — обновляем, если он существует
    if (statusWay) updateStatusSelect(statusWay, statusesPurchasing_method, currentWay);
    if (statusSelect) updateStatusSelect(statusSelect, statusesList, currentStatus);
    if (statusKTSSR) updateStatusSelect(statusKTSSR, statusesKTSSR, currentKTSSR);
    if (statusDopFC) updateStatusSelect(statusDopFC, statusesDopFC, currentDopFC);
    if (statusKOSGU) updateStatusSelect(statusKOSGU, statusesKOSGU, currentKOSGU);

    updateMandatoryFields(currentStatus, statusesMandatory);
    updateBlockingFields(currentStatus, statusesBlocking);

    console.log("Завершение script_add_edit.js");
}

function updateStatusSelect(selectElement, statuses, currentStatus) {
    selectElement.innerHTML = '';

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Выберите статус';
    if (currentStatus === '') defaultOption.selected = true;
    selectElement.appendChild(defaultOption);

    statuses.forEach(status => {
        const option = document.createElement('option');
        option.value = status;
        option.textContent = status;
        if (status === currentStatus) option.selected = true;
        selectElement.appendChild(option);
    });
}

function updateMandatoryFields(status, statusesMandatory) {
    const isMandatory = statusesMandatory.includes(status);
    const mandatoryFields = ['counterparty', 'contract_number', 'contract_date', 'end_date'];

    mandatoryFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field) return;

        if (isMandatory) {
            field.setAttribute('required', 'required');
        } else {
            field.removeAttribute('required');
        }
    });
}

function updateBlockingFields(status, statusesBlocking) {
    const isBlocked = statusesBlocking.includes(status);

    const fieldsToBlock = [
        'date_january_one', 'sum_january_one',
        'date_february', 'sum_february',
        'date_march', 'sum_march',
        'date_april', 'sum_april',
        'date_may', 'sum_may',
        'date_june', 'sum_june',
        'date_july', 'sum_july',
        'date_august', 'sum_august',
        'date_september', 'sum_september',
        'date_october', 'sum_october',
        'date_november', 'sum_november',
        'date_december', 'sum_december',
        'date_january_two', 'sum_january_two'
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