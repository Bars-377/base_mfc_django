const socket = new WebSocket("ws://172.18.11.104:8900/ws/some_path/"); // Инициализация WebSocket
console.log("Сокет инициализирован");

socket.onopen = function () {
	console.log("WebSocket подключен!");
};

socket.onerror = function (error) {
	console.log("Ошибка WebSocket:", error);
};

document.addEventListener("DOMContentLoaded", function () {
	const exportButton = document.getElementById("export-button");
	// const flashMessage = document.getElementById("flash-message");
	const message = document.getElementById("flash-message");
	let requestInProgress = false;
	let taskId = null;
	let checkStatusInterval = null;

	exportButton.onclick = function (event) {
		event.preventDefault();

		if (requestInProgress) {
			console.log("Запрос уже выполняется, новая отправка отменена");
			return;
		}

		requestInProgress = true;
		console.log("Запрос на экспорт начат");

		// Показать сообщение об ошибке

		message.textContent = "Пожалуйста, подождите, идёт загрузка!";

		// // Меняем класс на ошибку
		// message.classList.remove("alert-success");
		// message.classList.add("alert-danger");
		message.classList.add("alert-success");

		message.style.display = "block";

		const form = document.getElementById("export-form");

		if (!form) {
			console.error("Ошибка: форма не найдена!", form);
			return;
		}

		const formData = new FormData(form);
		const contract_date = formData.get("contract_date");
		const end_date = formData.get("end_date");

		console.log(`Отправка запроса на экспорт для года: ${contract_date} и ${end_date}`);

		// Отправка JSON через WebSocket
		socket.send(
			JSON.stringify({
				action: "export_excel",
				contract_date: contract_date,
				end_date: end_date,
			})
		);
	};

	// Получение сообщений от сервера
	socket.onmessage = function (event) {
		const data = JSON.parse(event.data);

		if (data.type === "export_started") {
			taskId = data.task_id;
			console.log(`Экспорт начат, ID задачи: ${taskId}`);

			checkStatusInterval = setInterval(function () {
				console.log(`Проверка статуса задачи с ID: ${taskId}`);
				socket.send(JSON.stringify({ action: "check_task_status", task_id: taskId }));
			}, 2000);
		}

		if (data.type === "export_success") {
			console.log(`Экспорт завершён успешно: ${data.filename}`);
			clearInterval(checkStatusInterval);

			const link = document.createElement("a");
			link.href = data.file_url;
			link.download = data.filename;
			link.click();

			message.textContent = "Экспорт завершен!";

			// // Меняем класс на ошибку
			// message.classList.remove("alert-success");
			// message.classList.add("alert-danger");
			message.classList.add("alert-success");

			message.style.display = "block";

			requestInProgress = false;
		}

		if (data.type === "export_error") {
			console.log("Произошла ошибка формирования файла:", data.message);

			message.textContent = data.message;

			// // Меняем класс на ошибку
			// message.classList.remove("alert-success");
			// message.classList.add("alert-danger");
			message.classList.add("alert-danger");

			message.style.display = "block";

			requestInProgress = false;
		}

		if (data.type === "task_status_pending") {
			console.log("Ожидание выполнения... Файл очень большой.");

			message.textContent = "В ожидании... Очень большой объём файла!";

			// // Меняем класс на ошибку
			// message.classList.remove("alert-success");
			// message.classList.add("alert-danger");
			message.classList.add("alert-success");

			message.style.display = "block";

		}

		if (data.type === "task_status_failure") {
			console.log("Ошибка экспорта!");

			message.textContent = "Ошибка экспорта!";

			// // Меняем класс на ошибку
			// message.classList.remove("alert-success");
			// message.classList.add("alert-danger");
			message.classList.add("alert-danger");

			message.style.display = "block";

			requestInProgress = false;
			clearInterval(checkStatusInterval);
		}

		// Добавлена обработка разрыва соединения
		if (data.type === "disconnect") {
			console.log("Соединение потеряно. Экспорт отменён!");

			message.textContent = "Соединение потеряно. Экспорт отменён!";

			// // Меняем класс на ошибку
			// message.classList.remove("alert-success");
			// message.classList.add("alert-danger");
			message.classList.add("alert-danger");

			message.style.display = "block";

			requestInProgress = false;
			clearInterval(checkStatusInterval);
		}
	};
});

document.addEventListener("DOMContentLoaded", function () {
	function formatNumbersInText() {
		const regex = /\d{1,3}(?:[.,]?\d{3})*(?:[.,]?\d+)?/g; // Поиск чисел с запятыми и точками

		// Получаем все текстовые узлы на странице
		const elements = document.querySelectorAll('*');

		elements.forEach(element => {
			if (element.getAttribute('data-type') === "no_format") {
				return; // Возвращаем, чтобы пропустить обработку этого элемента
			}
			// Проверяем, есть ли текстовое содержимое
			if (element.childNodes.length > 0) {
				element.childNodes.forEach(node => {
					if (node.nodeType === Node.TEXT_NODE) {
						node.nodeValue = node.nodeValue.replace(regex, match => {
							let num = parseFloat(match.replace(',', '.')); // Меняем запятую на точку
							let formatted = !isNaN(num) ? new Intl.NumberFormat("ru-RU", {
								minimumFractionDigits: match.includes('.') ? 2 : 0, // Две цифры после запятой, если есть дробная часть
								maximumFractionDigits: 2
							}).format(num) : match;
							return formatted.replace(/,/g, '.'); // Заменяем запятые на точки на выходе
						});
					}
				});
			}
		});
	}

	formatNumbersInText(); // Запускаем для всего документа
});

document.addEventListener("DOMContentLoaded", function () {
	document.querySelectorAll('.text-content').forEach(textContent => {
		const button = textContent.nextElementSibling; // Получаем кнопку рядом с текстом

		// Проверяем, обрезается ли текст
		if (textContent.scrollHeight <= textContent.clientHeight) {
			button.style.display = 'none'; // Скрываем кнопку, если текст полностью вмещается
		} else {
			button.style.display = 'block'; // Показываем кнопку, если текст обрезан
		}

		// Добавляем обработчик клика для показа и скрытия текста
		button.addEventListener('click', function () {
			textContent.classList.toggle('expanded');

			// Перепроверяем высоту после раскрытия
			this.textContent = textContent.classList.contains('expanded') ? 'Скрыть' : 'Показать больше';
		});
	});
});


function updateFileName() {
	const fileInput = document.getElementById('file-input');
	const fileNameDisplay = document.getElementById('file-name');

	if (fileInput.files.length > 0) {
		// Устанавливаем текстовое содержимое
		fileNameDisplay.textContent = "Выбран файл: " + fileInput.files[0].name;

		fileNameDisplay.style.display = 'inline-block';
		fileNameDisplay.style.verticalAlign = 'middle';
		// Применяем активные стили через fileNameDisplay.style
		fileNameDisplay.style.border = '2px solid red'; // Увеличиваем толщину рамки
		fileNameDisplay.style.padding = '8px 12px'; // Увеличиваем отступы

		fileNameDisplay.style.borderRadius = '5px'; // Скругляем углы

		fileNameDisplay.style.marginTop = '0';
		fileNameDisplay.style.marginRight = '10px';
		fileNameDisplay.style.marginBottom = '20px';
		fileNameDisplay.style.marginLeft = '10px';

		// Показываем кнопку отправки
		document.getElementById('submit-button').style.display = 'inline';
	} else {
		// Очищаем текстовое содержимое
		fileNameDisplay.textContent = '';

		fileNameDisplay.style.display = '';
		fileNameDisplay.style.verticalAlign = '';
		// Сбрасываем все стили
		fileNameDisplay.style.border = '';
		fileNameDisplay.style.padding = '';

		fileNameDisplay.style.borderRadius = '';

		fileNameDisplay.style.marginTop = '';
		fileNameDisplay.style.marginRight = '';
		fileNameDisplay.style.marginBottom = '';
		fileNameDisplay.style.marginLeft = '';

		// Скрываем кнопку отправки
		document.getElementById('submit-button').style.display = 'none';
	}
}

function showFlashMessage(event) {
	event.preventDefault();

	const fileInput = document.getElementById("file-input");
	if (fileInput.files.length === 0) {
		alert("Выберите файл перед отправкой!");
		return;
	}

	// Показываем индикатор загрузки
	const loadingIndicator = document.getElementById("loading");
	loadingIndicator.style.display = "block";

	const formData = new FormData();
	formData.append("file", fileInput.files[0]);

	fetch("/upload/", {  // URL на Django view
		method: "POST",
		body: formData,
		headers: {
			"X-CSRFToken": getCookie("csrftoken")
		}
	})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				// Скрыть индикатор загрузки с небольшой задержкой
				setTimeout(() => {
					console.log("Скрываю индикатор загрузки...");
					loadingIndicator.style.display = "none";
				}, 500); // Задержка 500ms

				// Показать сообщение
				const message = document.getElementById("flash-message");
				message.textContent = data.message;

				// Меняем класс в зависимости от статуса
				if (data.status === "success") {
					message.classList.remove("alert-danger");  // Убираем класс ошибки
					message.classList.add("alert-success");    // Добавляем класс успеха
					console.log("Status from server:", data.status);
				} else {
					message.classList.remove("alert-success");  // Убираем класс ошибки
					message.classList.add("alert-danger");     // Добавляем класс ошибки
					console.log("Status from server:", data.status);
				}

				message.style.display = "block";

				// Перезагрузка страницы через window.location.assign
				setTimeout(() => {
					window.location.assign(window.location.href);  // Переход на текущий URL, что вызывает перезагрузку
				}, 4000);  // Задержка 4 секунда, чтобы успело отобразиться сообщение
			} else {
				console.error("Ошибка:", data);
			}
		})
		.catch(error => {
			// Скрыть индикатор загрузки
			loadingIndicator.style.display = "none";

			// Показать сообщение об ошибке
			const message = document.getElementById("flash-message");
			message.textContent = "У вас недостаточно прав для этого действия!";

			// Меняем класс на ошибку
			message.classList.remove("alert-success");
			message.classList.add("alert-danger");

			message.style.display = "block";

			console.error("Ошибка загрузки файла:", error);
		});
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
	// const formData = new FormData();
	// formData.append('total_pages_full', currentPage); // Отправляем как POST

	// Формируем URL с параметрами GET
	const url = new URL(window.location.href);
	url.searchParams.set('contract_date', 'No');
	url.searchParams.set('end_date', 'No');
	url.searchParams.set('keyword_one', '');
	url.searchParams.set('keyword_two', '');
	url.searchParams.set('selected_column_one', '');
	url.searchParams.set('selected_column_two', '');
	url.searchParams.set('total_pages_full', currentPage);

	window.location.href = url; // Перезагружаем страницу с GET параметрами

	// Отправляем запрос через fetch
	// fetch(window.location.pathname, {
	// 	method: 'POST',
	// 	body: formData
	// }).then(() => {
	// 	window.location.href = url; // Перезагружаем страницу с GET параметрами
	// });
}

// Функция сброса фильтров и прокрутки
function resetFiltersUser() {
	// Сохраняем текущую позицию прокрутки
	sessionStorage.setItem('scrollPosition', window.scrollY);

	// Получаем текущую страницу
	const currentPage = new URLSearchParams(window.location.search).get('page_user') || 1;

	// Создаем объект для передачи данных через POST
	// const formData = new FormData();
	// formData.append('total_pages_full_user', currentPage); // Отправляем как POST

	// Формируем URL с параметрами GET
	const url = new URL(window.location.href);
	url.searchParams.set('KOSGU_user', 'No');

	url.searchParams.set('keyword_one_user', '');
	url.searchParams.set('keyword_two_user', '');
	url.searchParams.set('selected_column_one_user', '');
	url.searchParams.set('selected_column_two_user', '');
	url.searchParams.set('total_pages_full_user', currentPage);

	window.location.href = url; // Перезагружаем страницу с GET параметрами

	// Отправляем запрос через fetch
	// fetch(window.location.pathname, {
	// 	method: 'POST',
	// 	body: formData
	// }).then(() => {
	// 	window.location.href = url; // Перезагружаем страницу с GET параметрами
	// });
}

// Функция сброса фильтров и прокрутки
function resetFiltersUserTwo() {
	// Сохраняем текущую позицию прокрутки
	sessionStorage.setItem('scrollPosition', window.scrollY);

	// Получаем текущую страницу
	const currentPage = new URLSearchParams(window.location.search).get('page_user_two') || 1;

	// Создаем объект для передачи данных через POST
	// const formData = new FormData();
	// formData.append('total_pages_full_user_two', currentPage); // Отправляем как POST

	// Формируем URL с параметрами GET
	const url = new URL(window.location.href);
	url.searchParams.set('KOSGU_user_two', 'No');

	url.searchParams.set('keyword_one_user_two', '');
	url.searchParams.set('keyword_two_user_two', '');
	url.searchParams.set('selected_column_one_user_two', '');
	url.searchParams.set('selected_column_two_user_two', '');
	url.searchParams.set('total_pages_full_user_two', currentPage);

	window.location.href = url; // Перезагружаем страницу с GET параметрами

	// Отправляем запрос через fetch
	// fetch(window.location.pathname, {
	// 	method: 'POST',
	// 	body: formData
	// }).then(() => {
	// 	window.location.href = url; // Перезагружаем страницу с GET параметрами
	// });
}

// Функция обновления цвета строки
function updateColor(rowId, color) {
	console.log('data');
	fetch(`/update_color/${rowId}/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCookie('csrftoken')
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
		.catch(error => {
			alert('У вас нет прав для обновления цвета');
			console.error('Ошибка:', error)
		});
}

// Функция обновления цвета строки
function updateColorUser(rowId, color) {
	console.log('data');
	fetch(`/update_color_user/${rowId}/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCookie('csrftoken')
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
			'X-CSRFToken': getCookie('csrftoken')
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

		// 		// Проверяем существование поля ввода 1 перед обрезкой пробелов
		// 		const keywordInputOne = document.getElementById('keyword_one');
		// 		if (keywordInputOne) {
		// 			keywordInputOne.value = keywordInputOne.value.trim();
		// 		}

		// 		// Проверяем существование поля ввода 2 перед обрезкой пробелов
		// 		const keywordInputTwo = document.getElementById('keyword_two');
		// 		if (keywordInputTwo) {
		// 			keywordInputTwo.value = keywordInputTwo.value.trim();
		// 		}
	});
}

// Обработчик нажатия на кнопку фильтрации
const filterFormOne = document.getElementById('filter-form-user');
if (filterFormOne) {
	filterFormOne.addEventListener('submit', function () {
		// Сохраняем текущую позицию прокрутки
		sessionStorage.setItem('scrollPosition', window.scrollY);

		// 		// Проверяем существование поля ввода 1 перед обрезкой пробелов
		// 		const keywordInputOne = document.getElementById('keyword_one_user');
		// 		if (keywordInputOne) {
		// 			keywordInputOne.value = keywordInputOne.value.trim();
		// 		}

		// 		// Проверяем существование поля ввода 2 перед обрезкой пробелов
		// 		const keywordInputTwo = document.getElementById('keyword_two_user');
		// 		if (keywordInputTwo) {
		// 			keywordInputTwo.value = keywordInputTwo.value.trim();
		// 		}
	});
}

// Обработчик нажатия на кнопку фильтрации
const filterFormTwo = document.getElementById('filter-form-user-two');
if (filterFormTwo) {
	filterFormTwo.addEventListener('submit', function () {
		// Сохраняем текущую позицию прокрутки
		sessionStorage.setItem('scrollPosition', window.scrollY);

		// 		// Проверяем существование поля ввода 1 перед обрезкой пробелов
		// 		const keywordInputOne = document.getElementById('keyword_one_user_two');
		// 		if (keywordInputOne) {
		// 			keywordInputOne.value = keywordInputOne.value.trim();
		// 		}

		// 		// Проверяем существование поля ввода 2 перед обрезкой пробелов
		// 		const keywordInputTwo = document.getElementById('keyword_two_user_two');
		// 		if (keywordInputTwo) {
		// 			keywordInputTwo.value = keywordInputTwo.value.trim();
		// 		}
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

document.addEventListener('DOMContentLoaded', function () {
	const topScrolls = document.querySelectorAll('.top-scroll');
	const mainScrolls = document.querySelectorAll('.main-scroll');
	const scrollContents = document.querySelectorAll('.scroll-content');

	topScrolls.forEach((topScroll, index) => {
		const mainScroll = mainScrolls[index];
		const scrollContent = scrollContents[index];

		if (mainScroll && scrollContent) {
			// Устанавливаем ширину верхней прокрутки под ширину таблицы
			scrollContent.style.width = mainScroll.scrollWidth + 'px';

			// Синхронизация прокрутки
			topScroll.addEventListener('scroll', () => {
				mainScroll.scrollLeft = topScroll.scrollLeft;
			});

			mainScroll.addEventListener('scroll', () => {
				topScroll.scrollLeft = mainScroll.scrollLeft;
			});
		}
	});
});

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.startsWith(name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
	const deleteButtons = document.querySelectorAll('.delete-button');

	deleteButtons.forEach(button => {
		button.addEventListener('click', function () {
			const form = this.closest('.delete-form');
			const serviceId = form.getAttribute('data-id');
			console.log(`Ищем элемент с id: ${serviceId}`);

			if (confirmDelete()) {
				fetch(`/delete_record/${serviceId}/`, {  // Убедитесь, что здесь правильный путь
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRFToken': getCookie('csrftoken')
					},
					body: JSON.stringify({ id: serviceId })  // Отправка данных, если необходимо
				})
					.then(response => response.json()) // Преобразуем ответ в JSON
					.then(data => {
						if (data.success) { // Предполагаем, что сервер возвращает { success: true } при успешном удалении
							const row = document.querySelector(`.service-row[data-id="${serviceId}"]`);
							console.log(row); // Проверьте, что элемент найден
							if (row) {
								row.remove();
							}
							alert('Элемент успешно удален!'); // Уведомление об успешном удалении
							window.location.reload(); // Обновление страницы
						} else {
							alert('Ошибка:', data); // Если success не true
						}
					})
					.catch(error => {
						alert('У вас недостаточно прав для этого действия!');
						console.error('Ошибка:', error);
					});
			}
		});
	});
});

document.addEventListener('DOMContentLoaded', function () {
	const deleteButtons = document.querySelectorAll('.delete-button-user');

	deleteButtons.forEach(button => {
		button.addEventListener('click', function () {
			const form = this.closest('.delete-form-user');
			const serviceId = form.getAttribute('data-id');
			console.log(`Ищем элемент с id: ${serviceId}`);

			if (confirmDelete()) {
				fetch(`/delete_record_two/${serviceId}/`, {  // Убедитесь, что здесь правильный путь
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRFToken': getCookie('csrftoken')
					},
					body: JSON.stringify({ id: serviceId })  // Отправка данных, если необходимо
				})
					.then(response => {
						if (response.ok) {
							const row = document.querySelector(`.service-row-user[data-id="${serviceId}"]`);
							if (row) {
								row.remove();
							}
							alert('Элемент успешно удален!'); // Уведомление об успешном удалении
							window.location.reload(); // Обновление страницы
						} else {
							alert('Ошибка:', data); // Если success не true
						}
					})
					.catch(error => {
						alert('У вас недостаточно прав для этого действия!');
						console.error('Ошибка:', error);
					});
			}
		});
	});
});