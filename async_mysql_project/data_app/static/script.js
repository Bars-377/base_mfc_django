// const socket = io();  // Инициализация сокета
// console.log('Сокет инициализирован'); // Лог инициализации сокета

// document.addEventListener('DOMContentLoaded', function () {
// 	const exportButton = document.getElementById('export-button');
// 	let requestInProgress = false; // Флаг, указывающий на статус запроса
// 	let taskId = null; // ID задачи Celery

// 	exportButton.onclick = function (event) {
// 		event.preventDefault();  // Предотвращаем стандартное поведение кнопки

// 		// Проверяем, есть ли уже активный запрос
// 		if (requestInProgress) {
// 			console.log('Запрос уже выполняется, новая отправка отменена'); // Лог если запрос в процессе
// 			return; // Если запрос в процессе, просто выходим
// 		}

// 		// Устанавливаем флаг, что запрос начат
// 		requestInProgress = true;
// 		console.log('Запрос на экспорт начат'); // Лог начала запроса

// 		// Отображаем сообщение сразу после нажатия на кнопку
// 		const flashMessage = document.getElementById('flash-message');
// 		flashMessage.innerText = 'Пожалуйста, подождите, идёт загрузка!';
// 		flashMessage.style.display = 'block'; // Убедитесь, что сообщение отображается

// 		// Создаем временный элемент формы для отправки
// 		const form = document.getElementById('export-form');
// 		const formData = new FormData(form);

// 		// Извлекаем значение года из FormData
// 		const year = formData.get('year');
// 		const date_number_no_one = formData.get('date_number_no_one');
// 		console.log(`Отправка запроса на экспорт для года: ${year}`); // Лог года

// 		// Отправляем запрос на сервер через WebSocket
// 		socket.emit('export_excel', { year: year, date_number_no_one: date_number_no_one });
// 	};

// 	// Обработка события 'export_started' от сервера, где передается task_id
// 	socket.once('export_started', function(data) {
// 		taskId = data.task_id; // Сохраняем ID задачи
// 		console.log(`Экспорт начат, ID задачи: ${taskId}`); // Лог ID задачи

// 		// Теперь нужно периодически проверять статус задачи по taskId
// 		const checkStatusInterval = setInterval(function() {
// 			console.log(`Проверка статуса задачи с ID: ${taskId}`); // Лог проверки статуса
// 			// Отправляем запрос на проверку статуса задачи
// 			socket.emit('check_task_status', { task_id: taskId });
// 		}, 2000); // Проверяем каждые 2 секунды

// 		// Остановка проверки после получения результата
// 		socket.once('export_success', function(data) {
// 			console.log(`Экспорт завершён успешно: ${data.filename}`); // Лог успешного завершения
// 			clearInterval(checkStatusInterval); // Останавливаем проверку

// 			// Создаем ссылку для скачивания файла
// 			const link = document.createElement('a');
// 			link.href = data.file_url; // Используем URL для скачивания файла
// 			link.download = data.filename;
// 			link.click();

// 			// Скрываем сообщение после успешной загрузки
// 			const flashMessage = document.getElementById('flash-message');
// 			flashMessage.innerText = 'Экспорт завершен!';
// 			flashMessage.style.display = 'block';

// 			// Сбрасываем флаг после завершения загрузки
// 			requestInProgress = false;
// 		});

// 		// Обработка потери соединения
// 		socket.once('disconnect', function() {
// 			console.log('Соединение потеряно'); // Лог потери соединения
// 			const flashMessage = document.getElementById('flash-message');
// 			flashMessage.innerText = 'Соединение потеряно. Экспорт отменён!';
// 			flashMessage.style.display = 'block';

// 			// Сбрасываем флаг при потере соединения
// 			requestInProgress = false; // Разрешаем отправку нового запроса
// 		});

// 		// Обработка потери соединения
// 		socket.once('task_status_pending', function() {
// 			console.log('В ожидании.. Очень большой объём файла!'); // Лог потери соединения
// 			const flashMessage = document.getElementById('flash-message');
// 			flashMessage.innerText = 'В ожидании.. Очень большой объём файла!';
// 			flashMessage.style.display = 'block';
// 		});

// 		// Обработка потери соединения
// 		socket.once('task_status_failure', function() {
// 			console.log('Отказ!'); // Лог потери соединения
// 			const flashMessage = document.getElementById('flash-message');
// 			flashMessage.innerText = 'Отказ!';
// 			flashMessage.style.display = 'block';
// 		});

// 		// Обработка потери соединения
// 		socket.once('export_error', function(data) {
// 			console.log('Произошла ошибка формирования файла!'); // Лог потери соединения
// 			const flashMessage = document.getElementById('flash-message');
// 			flashMessage.innerText = data.message;
// 			flashMessage.style.display = 'block';
// 		});

// 	});

// });

function showFlashMessage(event) {

	// Показываем сообщение
	const flashMessage = document.getElementById('flash-message');
	flashMessage.style.display = 'block';

}

window.onload = function () {
	window.scrollTo(0, 0);
};

// Функция сброса фильтров и прокрутки
function resetFilters() {
	// Получаем текущую страницу
	const currentPage = new URLSearchParams(window.location.search).get('page') || 1;

	// Сбрасываем значения фильтров
	document.getElementById('contract_date').value = '';
	document.getElementById('end_date').value = '';
	document.getElementById('keyword_one').value = '';
	document.getElementById('keyword_two').value = '';
	document.getElementById('selected_column_one').value = '';
	document.getElementById('selected_column_two').value = '';

	// Добавляем текущую страницу как скрытое поле
	const pageInput = document.createElement('input');
	pageInput.type = 'hidden';
	pageInput.name = 'total_pages_full';
	pageInput.value = currentPage;

	const form = document.getElementById('filter-form');
	form.appendChild(pageInput);

	// Отправляем форму
	form.submit();
	window.scrollTo(0, 0);
}

// Функция обновления цвета строки
function updateColor(rowId, color) {
	console.log('data');
	fetch(`/update_color/${rowId}/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ color: color })
	})
		.then(response => response.json())
		.then(data => {
			console.log(data); // Добавьте эту строку
			if (data.success) {
				const row = document.querySelector(`.service-row[data-id="${data.id}"]`);
				if (row) {
					row.style.backgroundColor = data.color;
					const cells = row.querySelectorAll('td');
					// Изменение цвета всех ячеек, кроме последних двух
					const cellsToUpdate = Array.from(cells).slice(0, -2);
					cellsToUpdate.forEach(cell => {
						cell.style.backgroundColor = data.color;
					});
				}
			} else {
				console.log('rowId:', rowId, 'color:', color);
				alert('Не удалось обновить цвет');
			}
		})
		.catch(error => console.error('Ошибка:', error));
}

function confirmDelete() {
	return confirm('Вы уверены, что хотите удалить этот элемент?');
}

document.addEventListener('DOMContentLoaded', function () {
	const colorSelects = document.querySelectorAll('.color-select');

	colorSelects.forEach(select => {
		select.addEventListener('change', function () {
			const rowId = this.getAttribute('data-id');
			const selectedColor = this.value;

			updateColor(rowId, selectedColor);
		});
	});

	// Восстановление позиции скролла
	const scrollPosition = localStorage.getItem('scrollPosition');
	if (scrollPosition) {
		window.scrollTo(0, scrollPosition);
	}
});

window.addEventListener('beforeunload', function () {
	// Сохранение позиции скролла
	localStorage.setItem('scrollPosition', window.scrollY);
});

// Обработчик нажатия на кнопку сброса фильтров
document.getElementById('reset-filters').addEventListener('click', function () {
	resetFilters();
});

// Обработчик нажатия на кнопку фильтрации
document.getElementById('filter-form').addEventListener('submit', function (event) {
	window.scrollTo(0, 0);
	// Обрезаем пробелы с двух сторон поля ввода 1
	var keywordInput_one = document.getElementById('keyword_one');
	keywordInput_one.value = keywordInput_one.value.trim();
	// Обрезаем пробелы с двух сторон поля ввода 2
	var keywordInput_two = document.getElementById('keyword_two');
	keywordInput_two.value = keywordInput_two.value.trim();
});

document.addEventListener('DOMContentLoaded', function () {
	if (!navigator.userAgent.includes('AppleWebKit')) {
		document.querySelector('.wrapper').innerHTML = '<p>Sorry! Non webkit users.</p>';
	}
});

// Прокрутка таблицы при нажатии левой кнопки мыши
document.addEventListener('DOMContentLoaded', function () {
	const scrollContainer = document.querySelector('.scroll-container');
	let isMouseDown = false;
	let startX;
	let scrollLeft;

	scrollContainer.addEventListener('mousedown', (e) => {
		console.log('Mouse down'); // Добавлено для отладки
		isMouseDown = true;
		startX = e.pageX - scrollContainer.offsetLeft;
		scrollLeft = scrollContainer.scrollLeft;
		scrollContainer.style.cursor = 'grabbing';
	});

	scrollContainer.addEventListener('mouseleave', () => {
		isMouseDown = false;
		scrollContainer.style.cursor = 'default';
	});

	document.addEventListener('mouseup', () => {
		isMouseDown = false;
		scrollContainer.style.cursor = 'default';
	});

	scrollContainer.addEventListener('mousemove', (e) => {
		console.log('Mouse move'); // Добавлено для отладки
		if (!isMouseDown) return;
		e.preventDefault();
		const x = e.pageX - scrollContainer.offsetLeft;
		const walk = (x - startX) * 2; // Скорость прокрутки
		scrollContainer.scrollLeft = scrollLeft - walk;
	});
});

document.addEventListener('DOMContentLoaded', function () {
	const deleteButtons = document.querySelectorAll('.delete-button');

	deleteButtons.forEach(button => {
		button.addEventListener('click', function () {
			const form = this.closest('.delete-form');
			const serviceId = form.getAttribute('data-id');
			console.log(serviceId);

			if (confirmDelete()) {
				fetch(`/delete_record/${serviceId}/`, {  // Убедитесь, что здесь правильный путь
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({ id: serviceId })  // Отправка данных, если необходимо
				})
					.then(response => {
						if (response.ok) {
							const row = document.querySelector(`.service-row[data-id="${serviceId}"]`);
							if (row) {
								row.remove();
							}
							alert('Элемент успешно удален!'); // Уведомление об успешном удалении
						} else {
							alert('Ошибка удаления');
						}
					})
					.catch(error => console.error('Ошибка:', error));
			}
		});
	});
});