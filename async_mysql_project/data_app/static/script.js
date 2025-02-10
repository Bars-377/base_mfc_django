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

// Восстанавливаем прокрутку после загрузки страницы
window.onload = function () {
	// Восстановление для scrollPosition
	const scrollPosition = sessionStorage.getItem('scrollPosition');
	if (scrollPosition !== null) {
		window.scrollTo(0, parseInt(scrollPosition, 10));
		sessionStorage.removeItem('scrollPosition');
	}
};

// Функция сброса фильтров и прокрутки
function resetFilters() {
	// Сохраняем текущую позицию прокрутки
	sessionStorage.setItem('scrollPosition', window.scrollY);

	// Получаем текущую страницу
	const currentPage = new URLSearchParams(window.location.search).get('page') || 1;

	// Создаем объект для передачи данных через POST
	const formData = new FormData();
	formData.append('total_pages_full', currentPage); // Отправляем как POST

	// Формируем URL с параметрами GET
	const url = new URL(window.location.href);
	url.searchParams.set('contract_date', 'No');
	url.searchParams.set('end_date', 'No');
	url.searchParams.set('keyword_one', '');
	url.searchParams.set('keyword_two', '');
	url.searchParams.set('selected_column_one', '');
	url.searchParams.set('selected_column_two', '');

	// Отправляем запрос через fetch
	fetch(window.location.pathname, {
		method: 'POST',
		body: formData
	}).then(() => {
		window.location.href = url; // Перезагружаем страницу с GET параметрами
	});
}

// Функция сброса фильтров и прокрутки
function resetFiltersUser() {
	// Сохраняем текущую позицию прокрутки
	sessionStorage.setItem('scrollPosition', window.scrollY);

	// Получаем текущую страницу
	const currentPage = new URLSearchParams(window.location.search).get('page_user') || 1;

	// Создаем объект для передачи данных через POST
	const formData = new FormData();
	formData.append('total_pages_full_user', currentPage); // Отправляем как POST

	// Формируем URL с параметрами GET
	const url = new URL(window.location.href);
	url.searchParams.set('KOSGU_user', 'No');

	url.searchParams.set('keyword_one', '');
	url.searchParams.set('keyword_two', '');
	url.searchParams.set('selected_column_one', '');
	url.searchParams.set('selected_column_two', '');

	// Отправляем запрос через fetch
	fetch(window.location.pathname, {
		method: 'POST',
		body: formData
	}).then(() => {
		window.location.href = url; // Перезагружаем страницу с GET параметрами
	});
}

// Функция сброса фильтров и прокрутки
function resetFiltersUserTwo() {
	// Сохраняем текущую позицию прокрутки
	sessionStorage.setItem('scrollPosition', window.scrollY);

	// Получаем текущую страницу
	const currentPage = new URLSearchParams(window.location.search).get('page_user_two') || 1;

	// Создаем объект для передачи данных через POST
	const formData = new FormData();
	formData.append('total_pages_full_user_two', currentPage); // Отправляем как POST

	// Формируем URL с параметрами GET
	const url = new URL(window.location.href);
	url.searchParams.set('KOSGU_user_two', 'No');

	url.searchParams.set('keyword_one', '');
	url.searchParams.set('keyword_two', '');
	url.searchParams.set('selected_column_one', '');
	url.searchParams.set('selected_column_two', '');

	// Отправляем запрос через fetch
	fetch(window.location.pathname, {
		method: 'POST',
		body: formData
	}).then(() => {
		window.location.href = url; // Перезагружаем страницу с GET параметрами
	});
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

// Функция обновления цвета строки
function updateColorUser(rowId, color) {
	console.log('data');
	fetch(`/update_color_user/${rowId}/`, {
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
				const row = document.querySelector(`.service-row-user[data-id="${data.id}"]`);
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

// Функция обновления цвета строки
function updateColorUserTwo(rowId, color) {
	console.log('data');
	fetch(`/update_color_user_two/${rowId}/`, {
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
				const row = document.querySelector(`.service-row-user-two[data-id="${data.id}"]`);
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
	// const scrollPosition = localStorage.getItem('scrollPosition');
	// if (scrollPosition) {
	// 	window.scrollTo(0, scrollPosition);
	// }
});

document.addEventListener('DOMContentLoaded', function () {
	const colorSelects = document.querySelectorAll('.color-select-user');

	colorSelects.forEach(select => {
		select.addEventListener('change', function () {
			const rowId = this.getAttribute('data-id');
			const selectedColor = this.value;

			updateColorUser(rowId, selectedColor);
		});
	});

	// Восстановление позиции скролла
	// const scrollPosition = localStorage.getItem('scrollPosition');
	// if (scrollPosition) {
	// 	window.scrollTo(0, scrollPosition);
	// }
});

document.addEventListener('DOMContentLoaded', function () {
	const colorSelects = document.querySelectorAll('.color-select-user-two');

	colorSelects.forEach(select => {
		select.addEventListener('change', function () {
			const rowId = this.getAttribute('data-id');
			const selectedColor = this.value;

			updateColorUserTwo(rowId, selectedColor);
		});
	});

	// Восстановление позиции скролла
	// const scrollPosition = localStorage.getItem('scrollPosition');
	// if (scrollPosition) {
	// 	window.scrollTo(0, scrollPosition);
	// }
});

window.addEventListener('beforeunload', function () {
	// Сохранение позиции скролла
	localStorage.setItem('scrollPosition', window.scrollY);
});

// Обработчик нажатия на кнопку сброса фильтров
const resetButton = document.getElementById('reset-filters');
if (resetButton) {
	resetButton.addEventListener('click', function () {
		resetFilters();
	});
}

// Обработчик нажатия на кнопку сброса фильтров
const resetButtonOne = document.getElementById('reset-filters-user');
if (resetButtonOne) {
	resetButtonOne.addEventListener('click', function () {
		resetFiltersUser();
	});
}

// Обработчик нажатия на кнопку сброса фильтров
const resetButtonTwo = document.getElementById('reset-filters-user-two');
if (resetButtonTwo) {
	resetButtonTwo.addEventListener('click', function () {
		resetFiltersUserTwo();
	});
}

// Обработчик нажатия на кнопку фильтрации
const filterForm = document.getElementById('filter-form');
if (filterForm) {
	filterForm.addEventListener('submit', function () {
		// Сохраняем текущую позицию прокрутки
		sessionStorage.setItem('scrollPosition', window.scrollY);

		// Проверяем существование поля ввода 1 перед обрезкой пробелов
		const keywordInputOne = document.getElementById('keyword_one');
		if (keywordInputOne) {
			keywordInputOne.value = keywordInputOne.value.trim();
		}

		// Проверяем существование поля ввода 2 перед обрезкой пробелов
		const keywordInputTwo = document.getElementById('keyword_two');
		if (keywordInputTwo) {
			keywordInputTwo.value = keywordInputTwo.value.trim();
		}
	});
}

// Обработчик нажатия на кнопку фильтрации
const filterFormOne = document.getElementById('filter-form-user');
if (filterFormOne) {
	filterFormOne.addEventListener('submit', function () {
		// Сохраняем текущую позицию прокрутки
		sessionStorage.setItem('scrollPosition', window.scrollY);

		// Проверяем существование поля ввода 1 перед обрезкой пробелов
		const keywordInputOne = document.getElementById('keyword_one_user');
		if (keywordInputOne) {
			keywordInputOne.value = keywordInputOne.value.trim();
		}

		// Проверяем существование поля ввода 2 перед обрезкой пробелов
		const keywordInputTwo = document.getElementById('keyword_two_user');
		if (keywordInputTwo) {
			keywordInputTwo.value = keywordInputTwo.value.trim();
		}
	});
}

// Обработчик нажатия на кнопку фильтрации
const filterFormTwo = document.getElementById('filter-form-user-two');
if (filterFormTwo) {
	filterFormTwo.addEventListener('submit', function () {
		// Сохраняем текущую позицию прокрутки
		sessionStorage.setItem('scrollPosition', window.scrollY);

		// Проверяем существование поля ввода 1 перед обрезкой пробелов
		const keywordInputOne = document.getElementById('keyword_one_user_two');
		if (keywordInputOne) {
			keywordInputOne.value = keywordInputOne.value.trim();
		}

		// Проверяем существование поля ввода 2 перед обрезкой пробелов
		const keywordInputTwo = document.getElementById('keyword_two_user_two');
		if (keywordInputTwo) {
			keywordInputTwo.value = keywordInputTwo.value.trim();
		}
	});
}

document.addEventListener('DOMContentLoaded', function () {
	if (!navigator.userAgent.includes('AppleWebKit')) {
		document.querySelector('.wrapper').innerHTML = '<p>Sorry! Non webkit users.</p>';
	}
});

// Прокрутка таблицы при нажатии левой кнопки мыши
document.addEventListener('DOMContentLoaded', function () {
	const scrollContainers = document.querySelectorAll('.scroll-container');

	scrollContainers.forEach((scrollContainer) => {
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
});

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
const csrftoken = getCookie('csrftoken');

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
						'Content-Type': 'application/json',
						'X-CSRFToken': csrftoken
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
							window.location.reload(); // Обновление страницы
						} else {
							alert('Ошибка удаления');
						}
					})
					.catch(error => console.error('Ошибка:', error));
			}
		});
	});
});

// document.addEventListener('DOMContentLoaded', function () {
// 	const deleteButtons = document.querySelectorAll('.delete-button-user');

// 	deleteButtons.forEach(button => {
// 		button.addEventListener('click', function () {
// 			const form = this.closest('.delete-form-user');
// 			const serviceId = form.getAttribute('data-id');
// 			console.log(serviceId);

// 			if (confirmDelete()) {
// 				fetch(`/delete_record/${serviceId}/`, {  // Убедитесь, что здесь правильный путь
// 					method: 'POST',
// 					headers: {
// 						'Content-Type': 'application/json'
// 					},
// 					body: JSON.stringify({ id: serviceId })  // Отправка данных, если необходимо
// 				})
// 					.then(response => {
// 						if (response.ok) {
// 							const row = document.querySelector(`.service-row-user[data-id="${serviceId}"]`);
// 							if (row) {
// 								row.remove();
// 							}
// 							alert('Элемент успешно удален!'); // Уведомление об успешном удалении
// 						} else {
// 							alert('Ошибка удаления');
// 						}
// 					})
// 					.catch(error => console.error('Ошибка:', error));
// 			}
// 		});
// 	});
// });