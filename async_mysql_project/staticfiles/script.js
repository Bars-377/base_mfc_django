const socket = new WebSocket(`ws://${connection_websocket}:8900/ws/some_path/`); // Инициализация WebSocket
console.log("Сокет инициализирован");

socket.onopen = function () {
	console.log("WebSocket подключен!");
};

socket.onerror = function (error) {
	console.log("Ошибка WebSocket:", error);
};

socket.onclose = function (event) {
	console.log("WebSocket закрыт:", event);
	// Выполните действия при закрытии соединения
};

document.addEventListener("DOMContentLoaded", function () {
	const exportButton = document.getElementById("export-button");
	// const flashMessage = document.getElementById("flash-message");
	const message = document.getElementById("flash-message-export");
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

			message.textContent = "Произошла ошибка формирования файла: " + data.message;

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
			console.log("Ошибка экспорта:", data.error);

			message.textContent = "Ошибка экспорта! " + data.error;

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

// document.addEventListener("DOMContentLoaded", function () {
// 	function formatNumbersInText() {
// 		const regex = /\d{1,3}(?:[.,]?\d{3})*(?:[.,]?\d+)?/g; // Поиск чисел с запятыми и точками

// 		// Получаем все текстовые узлы на странице
// 		const elements = document.querySelectorAll('*');

// 		elements.forEach(element => {
// 			if (element.getAttribute('data-type') === "no_format") {
// 				return; // Возвращаем, чтобы пропустить обработку этого элемента
// 			}
// 			// Проверяем, есть ли текстовое содержимое
// 			if (element.childNodes.length > 0) {
// 				element.childNodes.forEach(node => {
// 					if (node.nodeType === Node.TEXT_NODE) {
// 						node.nodeValue = node.nodeValue.replace(regex, match => {
// 							let num = parseFloat(match.replace(',', '.')); // Меняем запятую на точку
// 							let formatted = !isNaN(num) ? new Intl.NumberFormat("ru-RU", {
// 								minimumFractionDigits: match.includes('.') ? 2 : 0, // Две цифры после запятой, если есть дробная часть
// 								maximumFractionDigits: 2
// 							}).format(num) : match;
// 							return formatted.replace(/,/g, '.'); // Заменяем запятые на точки на выходе
// 						});
// 					}
// 				});
// 			}
// 		});
// 	}

// 	formatNumbersInText(); // Запускаем для всего документа
// });

document.addEventListener("DOMContentLoaded", function () {
	function formatNumbersInText() {
		const regex = /\d+(?:[.,]\d+)?/g; // Поиск чисел с точками или запятыми

		const elements = document.querySelectorAll('*');

		elements.forEach(element => {
			if (element.getAttribute('data-type') === "no_format") return;

			element.childNodes.forEach(node => {
				if (node.nodeType === Node.TEXT_NODE) {
					node.nodeValue = node.nodeValue.replace(regex, match => {
						// Заменяем запятую на точку для корректного парсинга
						let num = parseFloat(match.replace(',', '.'));

						if (isNaN(num)) return match;

						// Форматируем с пробелом в тысячах и двумя знаками после запятой
						let formatted = new Intl.NumberFormat('ru-RU', {
							minimumFractionDigits: 2,
							maximumFractionDigits: 2
						}).format(num);

						// Заменяем десятичный разделитель запятую на точку
						return formatted.replace(',', '.');
					});
				}
			});
		});
	}

	formatNumbersInText();
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

	const submitButton = document.getElementById('submit-button');
	submitButton.style.display = 'none';

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
					submitButton.style.display = 'inline-block';
				}, 500); // Задержка 500ms

				// Показать сообщение
				const message = document.getElementById("flash-message-import");
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
			submitButton.style.display = 'inline-block';

			// Показать сообщение об ошибке
			const message = document.getElementById("flash-message-import");
			message.textContent = "У вас недостаточно прав для этого действия!";

			// Меняем класс на ошибку
			message.classList.remove("alert-success");
			message.classList.add("alert-danger");

			message.style.display = "block";

			console.error("Ошибка загрузки файла:", error);
		});
}

// function hasSelectedFile() {
//     const fileInput = document.getElementById('file-input');
//     return fileInput.files.length > 0;
// }

// function updateFileName() {
//     const fileInput = document.getElementById('file-input');
//     const fileNameDisplay = document.getElementById('file-name');
//     const submitButton = document.getElementById('submit-button');

//     if (hasSelectedFile()) {
//         const fileName = fileInput.files[0].name;
//         fileNameDisplay.textContent = "Выбран файл: " + fileName;
//         fileNameDisplay.style.cssText = `
//             display: inline-block;
//             vertical-align: middle;
//             border: 2px solid red;
//             padding: 8px 12px;
//             border-radius: 5px;
//             margin: 0 10px 20px 10px;
//         `;
//         submitButton.style.display = 'inline-block';
//     } else {
//         fileNameDisplay.textContent = '';
//         fileNameDisplay.style.cssText = '';
//         submitButton.style.display = 'none';
//     }
// }

// function showFlashMessage(event) {
//     event.preventDefault();

//     if (!hasSelectedFile()) {
//         alert("Выберите файл перед отправкой!");
//         return;
//     }

// 	// Показываем индикатор загрузки
// 	const loadingIndicator = document.getElementById("loading");
// 	const submitButton = document.getElementById('submit-button');

// 	loadingIndicator.style.display = "block";
// 	submitButton.style.display = 'none';

// 	const formData = new FormData();
// 	formData.append("file", fileInput.files[0]);

// 	fetch("/upload/", {  // URL на Django view
// 		method: "POST",
// 		body: formData,
// 		headers: {
// 			"X-CSRFToken": getCookie("csrftoken")
// 		}
// 	})
// 		.then(response => response.json())
// 		.then(data => {
// 			if (data.success) {
// 				// Скрыть индикатор загрузки с небольшой задержкой
// 				setTimeout(() => {
// 					console.log("Скрываю индикатор загрузки...");
// 					loadingIndicator.style.display = "none";
// 					submitButton.style.display = 'inline-block';
// 				}, 500); // Задержка 500ms

// 				// Показать сообщение
// 				const message = document.getElementById("flash-message-import");
// 				message.textContent = data.message;

// 				// Меняем класс в зависимости от статуса
// 				if (data.status === "success") {
// 					message.classList.remove("alert-danger");  // Убираем класс ошибки
// 					message.classList.add("alert-success");    // Добавляем класс успеха
// 					console.log("Status from server:", data.status);
// 				} else {
// 					message.classList.remove("alert-success");  // Убираем класс ошибки
// 					message.classList.add("alert-danger");     // Добавляем класс ошибки
// 					console.log("Status from server:", data.status);
// 				}

// 				message.style.display = "block";

// 				// Перезагрузка страницы через window.location.assign
// 				setTimeout(() => {
// 					window.location.assign(window.location.href);  // Переход на текущий URL, что вызывает перезагрузку
// 				}, 4000);  // Задержка 4 секунда, чтобы успело отобразиться сообщение
// 			} else {
// 				console.error("Ошибка:", data);
// 			}
// 		})
// 		.catch(error => {
// 			// Скрыть индикатор загрузки
// 			loadingIndicator.style.display = "none";
// 			submitButton.style.display = 'inline-block';

// 			// Показать сообщение об ошибке
// 			const message = document.getElementById("flash-message-import");
// 			message.textContent = "У вас недостаточно прав для этого действия!";

// 			// Меняем класс на ошибку
// 			message.classList.remove("alert-success");
// 			message.classList.add("alert-danger");

// 			message.style.display = "block";

// 			console.error("Ошибка загрузки файла:", error);
// 		});
// }

document.addEventListener('DOMContentLoaded', function () {
	// Обработчик для кнопки "Резерв (Вторник)"
	document.getElementById('backup-one-button').addEventListener('click', function (e) {
		e.preventDefault();  // Предотвратить стандартное поведение кнопки

		// Подтверждение перед выполнением действия
		if (!confirm('Вы уверены, что хотите выполнить резервное копирование для вторника?')) {
			return;  // Прерываем выполнение, если пользователь нажал "Отмена"
		}

		// Получаем URL из data-атрибута
		const url = e.target.getAttribute('data-url');

		// Используем fetch для AJAX-запроса
		fetch(url, {
			method: 'GET',  // Метод запроса
		})
			.then(response => response.json())  // Преобразуем ответ в JSON
			.then(data => {
				if (data.success) {
					document.getElementById('flash-message-one').textContent = 'Удачно!';
					document.getElementById('flash-message-one').style.display = 'block';
					document.getElementById('flash-message-one').classList.remove('alert-danger');
					document.getElementById('flash-message-one').classList.add('alert-success');
					window.scrollTo(0, 0);  // Сбрасывает скролл на верх страницы
					window.location.reload(); // Обновление страницы
				} else {
					document.getElementById('flash-message-one').textContent = data.message || 'Произошла ошибка!';
					document.getElementById('flash-message-one').style.display = 'block';
					document.getElementById('flash-message-one').classList.remove('alert-success');
					document.getElementById('flash-message-one').classList.add('alert-danger');
				}
			})
			.catch(error => {
				document.getElementById('flash-message-one').textContent = 'У вас недостаточно прав для этого действия!';
				document.getElementById('flash-message-one').style.display = 'block';
				document.getElementById('flash-message-one').classList.remove('alert-success');
				document.getElementById('flash-message-one').classList.add('alert-danger');
			});
	});

	// Обработчик для кнопки "Резерв (Четверг)"
	document.getElementById('backup-two-button').addEventListener('click', function (e) {
		e.preventDefault();  // Предотвратить стандартное поведение кнопки

		// Подтверждение перед выполнением действия
		if (!confirm('Вы уверены, что хотите выполнить резервное копирование для четверга?')) {
			return;  // Прерываем выполнение, если пользователь нажал "Отмена"
		}

		// Получаем URL из data-атрибута
		const url = e.target.getAttribute('data-url');

		// Используем fetch для AJAX-запроса
		fetch(url, {
			method: 'GET',  // Метод запроса
		})
			.then(response => response.json())  // Преобразуем ответ в JSON
			.then(data => {
				if (data.success) {
					document.getElementById('flash-message-two').textContent = 'Удачно!';
					document.getElementById('flash-message-two').style.display = 'block';
					document.getElementById('flash-message-two').classList.remove('alert-danger');
					document.getElementById('flash-message-two').classList.add('alert-success');
					window.scrollTo(0, 0);  // Сбрасывает скролл на верх страницы
					window.location.reload(); // Обновление страницы
				} else {
					document.getElementById('flash-message-two').textContent = data.message || 'Произошла ошибка!';
					document.getElementById('flash-message-two').style.display = 'block';
					document.getElementById('flash-message-two').classList.remove('alert-success');
					document.getElementById('flash-message-two').classList.add('alert-danger');
				}
			})
			.catch(error => {
				document.getElementById('flash-message-two').textContent = 'У вас недостаточно прав для этого действия!';
				document.getElementById('flash-message-two').style.display = 'block';
				document.getElementById('flash-message-two').classList.remove('alert-success');
				document.getElementById('flash-message-two').classList.add('alert-danger');
			});
	});
});

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
	url.searchParams.set('keyword_three', '');
	url.searchParams.set('keyword_four', '');
	url.searchParams.set('selected_column_one', '');
	url.searchParams.set('selected_column_two', '');
	url.searchParams.set('selected_column_three', '');
	url.searchParams.set('selected_column_four', '');
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
	// url.searchParams.set('KOSGU_user', 'No');

	// url.searchParams.set('keyword_one_user', '');
	// url.searchParams.set('keyword_two_user', '');
	// url.searchParams.set('selected_column_one_user', '');
	// url.searchParams.set('selected_column_two_user', '');
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
	// url.searchParams.set('KOSGU_user_two', 'No');

	// url.searchParams.set('keyword_one_user_two', '');
	// url.searchParams.set('keyword_two_user_two', '');
	// url.searchParams.set('selected_column_one_user_two', '');
	// url.searchParams.set('selected_column_two_user_two', '');
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
		// document.querySelector('.wrapper').innerHTML = '<p>Sorry! Non webkit users.</p>';
		console.log('Sorry! Non webkit users!');
	}
});

// // Прокрутка таблицы при нажатии левой кнопки мыши
// document.addEventListener('DOMContentLoaded', function () {
// 	const scrollContainers = document.querySelectorAll('.scroll-container');

// 	scrollContainers.forEach((scrollContainer) => {
// 		let isMouseDown = false;
// 		let startX;
// 		let scrollLeft;

// 		scrollContainer.addEventListener('mousedown', (e) => {
// 			//console.log('Mouse down'); // Добавлено для отладки
// 			isMouseDown = true;
// 			startX = e.pageX - scrollContainer.offsetLeft;
// 			scrollLeft = scrollContainer.scrollLeft;
// 			scrollContainer.style.cursor = 'grabbing';
// 		});

// 		scrollContainer.addEventListener('mouseleave', () => {
// 			isMouseDown = false;
// 			scrollContainer.style.cursor = 'default';
// 		});

// 		document.addEventListener('mouseup', () => {
// 			isMouseDown = false;
// 			scrollContainer.style.cursor = 'default';
// 		});

// 		scrollContainer.addEventListener('mousemove', (e) => {
// 			//console.log('Mouse move'); // Добавлено для отладки
// 			if (!isMouseDown) return;
// 			e.preventDefault();
// 			const x = e.pageX - scrollContainer.offsetLeft;
// 			const walk = (x - startX) * 2; // Скорость прокрутки
// 			scrollContainer.scrollLeft = scrollLeft - walk;
// 		});
// 	});
// });

// Прокрутка таблицы при нажатии левой кнопки мыши
document.addEventListener('DOMContentLoaded', function () {
	const scrollContainers = document.querySelectorAll('.scroll-container');

	scrollContainers.forEach((scrollContainer, index) => {
		let isMouseDown = false;
		let isTextHovered = false;
		let startX;
		let scrollLeft;

		// console.log(`🌀 Инициализирован scrollContainer[${index}]`);

		const disableTextSelection = () => {
			document.body.style.userSelect = 'none';
			document.body.style.webkitUserSelect = 'none'; // Safari
		};

		const enableTextSelection = () => {
			document.body.style.userSelect = '';
			document.body.style.webkitUserSelect = '';
		};

		scrollContainer.addEventListener('mousedown', (e) => {
			if (isTextHovered) {
				// console.log('⛔ Прокрутка заблокирована — курсор над текстом');
				return;
			}
			isMouseDown = true;
			startX = e.pageX - scrollContainer.offsetLeft;
			scrollLeft = scrollContainer.scrollLeft;
			scrollContainer.style.cursor = 'grabbing';
			disableTextSelection();
			// console.log(`✅ Mousedown: startX=${startX}, scrollLeft=${scrollLeft}`);
		});

		scrollContainer.addEventListener('mouseleave', () => {
			isMouseDown = false;
			scrollContainer.style.cursor = 'default';
			enableTextSelection();
			// console.log('ℹ️ Mouseleave: остановка прокрутки');
		});

		document.addEventListener('mouseup', () => {
			if (isMouseDown) {
				// console.log('🛑 Mouseup: остановка прокрутки');
			}
			isMouseDown = false;
			scrollContainer.style.cursor = isTextHovered ? 'text' : 'grab';
			enableTextSelection();
		});

		scrollContainer.addEventListener('mousemove', (e) => {
			if (!isMouseDown) return;
			if (isTextHovered) {
				// console.log('⚠️ Прокрутка отменена — курсор над текстом');
				return;
			}
			e.preventDefault();
			const x = e.pageX - scrollContainer.offsetLeft;
			const walk = (x - startX) * 2;
			scrollContainer.scrollLeft = scrollLeft - walk;
			// console.log(`↔️ Прокрутка: x=${x}, walk=${walk}, scrollLeft=${scrollContainer.scrollLeft}`);
		});

		function hasVisibleTextUnderCursor(x, y, container) {
			const el = document.elementFromPoint(x, y);
			if (!el || !container.contains(el)) return false;

			const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, {
				acceptNode: function (node) {
					if (node.nodeValue.trim().length > 0) {
						const range = document.createRange();
						range.selectNodeContents(node);
						const rect = range.getBoundingClientRect();
						if (
							y >= rect.top && y <= rect.bottom &&
							x >= rect.left && x <= rect.right
						) {
							return NodeFilter.FILTER_ACCEPT;
						}
					}
					return NodeFilter.FILTER_SKIP;
				}
			});

			return !!walker.nextNode();
		}

		scrollContainer.addEventListener('mousemove', function (e) {
			const hasText = hasVisibleTextUnderCursor(e.clientX, e.clientY, scrollContainer);

			if (hasText && !isTextHovered) {
				isTextHovered = true;
				scrollContainer.style.cursor = 'text';
				// console.log('🟡 Наведён курсор прямо на видимый текст');
			} else if (!hasText && isTextHovered) {
				isTextHovered = false;
				scrollContainer.style.cursor = isMouseDown ? 'grabbing' : 'grab';
				// console.log('🔵 Курсор ушёл с текста — прокрутка разрешена');
			}
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

// document.addEventListener('DOMContentLoaded', function () {
// 	const deleteButtons = document.querySelectorAll('.delete-button');

// 	deleteButtons.forEach(button => {
// 		button.addEventListener('click', function () {
// 			const form = this.closest('.delete-form');
// 			const serviceId = form.getAttribute('data-id');

// 			const page = form.getAttribute('data-page');
// 			const keyword_one = form.getAttribute('data-keyword-one');
// 			const keyword_two = form.getAttribute('data-keyword-two');
// 			const keyword_three = form.getAttribute('data-keyword-three');
// 			const keyword_four = form.getAttribute('data-keyword-four');
// 			const selected_column_one = form.getAttribute('data-selected-column-one');
// 			const selected_column_two = form.getAttribute('data-selected-column-two');
// 			const contract_date = form.getAttribute('data-contract-date');
// 			const selected_end_date = form.getAttribute('data-selected-end-date');

// 			const page_user = form.getAttribute('data-page-user');

// 			const page_user_two = form.getAttribute('data-page-user-two');

// 			console.log(`Ищем элемент с id: ${serviceId}`);

// 			if (confirmDelete()) {
// 				fetch(`/delete_record/`, {  // Убедитесь, что здесь правильный путь
// 					method: 'POST',
// 					headers: {
// 						'Content-Type': 'application/json',
// 						'X-CSRFToken': getCookie('csrftoken')
// 					},
// 					body: JSON.stringify({
// 						id: serviceId,
// 						page: page,
// 						keyword_one: keyword_one,
// 						keyword_two: keyword_two,
// 						keyword_three: keyword_three,
// 						keyword_four: keyword_four,
// 						selected_column_one: selected_column_one,
// 						selected_column_two: selected_column_two,
// 						contract_date: contract_date,
// 						selected_end_date: selected_end_date,

// 						page_user: page_user,

// 						page_user_two: page_user_two,

// 					})  // Отправка данных, если необходимо
// 				})
// 					.then(response => response.json()) // Преобразуем ответ в JSON
// 					.then(data => {
// 						if (data.success) { // Предполагаем, что сервер возвращает { success: true } при успешном удалении
// 							const row = document.querySelector(`.service-row[data-id="${serviceId}"]`);
// 							console.log(row); // Проверьте, что элемент найден
// 							if (row) {
// 								row.remove();
// 							}
// 							alert('Элемент успешно удален!'); // Уведомление об успешном удалении
// 							window.location.reload(); // Обновление страницы
// 						} else {
// 							alert('Ошибка:', data); // Если success не true
// 						}
// 					})
// 					.catch(error => {
// 						alert('У вас недостаточно прав для этого действия!');
// 						console.error('Ошибка:', error);
// 					});
// 			}
// 		});
// 	});
// });

// document.addEventListener('DOMContentLoaded', function () {
// 	const deleteButtons = document.querySelectorAll('.delete-button');

// 	deleteButtons.forEach(button => {
// 		button.addEventListener('click', function () {
// 			const form = this.closest('.delete-form');
// 			const serviceId = form.getAttribute('data-id');

// 			const page = form.getAttribute('data-page');
// 			const keyword_one = form.getAttribute('data-keyword-one');
// 			const keyword_two = form.getAttribute('data-keyword-two');
// 			const keyword_three = form.getAttribute('data-keyword-three');
// 			const keyword_four = form.getAttribute('data-keyword-four');
// 			const selected_column_one = form.getAttribute('data-selected-column-one');
// 			const selected_column_two = form.getAttribute('data-selected-column-two');
// 			const contract_date = form.getAttribute('data-contract-date');
// 			const selected_end_date = form.getAttribute('data-selected-end-date');
// 			const page_user = form.getAttribute('data-page-user');
// 			const page_user_two = form.getAttribute('data-page-user-two');

// 			console.log(`Ищем элемент с id: ${serviceId}`);

// 			if (confirmDelete()) {
// 				// Показать блокирующий оверлей
// 				const overlay = document.getElementById('deletion-overlay');
// 				if (overlay) {
// 					overlay.style.display = 'flex';
// 				}

// 				fetch(`/delete_record/`, {
// 					method: 'POST',
// 					headers: {
// 						'Content-Type': 'application/json',
// 						'X-CSRFToken': getCookie('csrftoken')
// 					},
// 					body: JSON.stringify({
// 						id: serviceId,
// 						page: page,
// 						keyword_one: keyword_one,
// 						keyword_two: keyword_two,
// 						keyword_three: keyword_three,
// 						keyword_four: keyword_four,
// 						selected_column_one: selected_column_one,
// 						selected_column_two: selected_column_two,
// 						contract_date: contract_date,
// 						selected_end_date: selected_end_date,
// 						page_user: page_user,
// 						page_user_two: page_user_two,
// 					})
// 				})
// 				.then(response => response.json())
// 				.then(data => {
// 					if (overlay) overlay.style.display = 'none';

// 					if (data.success) {
// 						const row = document.querySelector(`.service-row[data-id="${serviceId}"]`);
// 						console.log(row);
// 						if (row) {
// 							row.remove();
// 						}
// 						alert('Элемент успешно удален!');
// 						window.location.reload();
// 					} else {
// 						alert('Ошибка: ' + JSON.stringify(data));
// 					}
// 				})
// 				.catch(error => {
// 					if (overlay) overlay.style.display = 'none';
// 					alert('У вас недостаточно прав для этого действия!');
// 					console.error('Ошибка:', error);
// 				});
// 			}
// 		});
// 	});
// });

// document.addEventListener('DOMContentLoaded', function () {
// 	const deleteButtons = document.querySelectorAll('.delete-button-user');

// 	deleteButtons.forEach(button => {
// 		button.addEventListener('click', function () {
// 			const form = this.closest('.delete-form-user');
// 			const serviceId = form.getAttribute('data-id');
// 			console.log(`Ищем элемент с id: ${serviceId}`);

// 			if (confirmDelete()) {
// 				fetch(`/delete_record_two/${serviceId}/`, {  // Убедитесь, что здесь правильный путь
// 					method: 'POST',
// 					headers: {
// 						'Content-Type': 'application/json',
// 						'X-CSRFToken': getCookie('csrftoken')
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
// 							window.location.reload(); // Обновление страницы
// 						} else {
// 							alert('Ошибка:', data); // Если success не true
// 						}
// 					})
// 					.catch(error => {
// 						alert('У вас недостаточно прав для этого действия!');
// 						console.error('Ошибка:', error);
// 					});
// 			}
// 		});
// 	});
// });

document.addEventListener('DOMContentLoaded', () => {
	const overlay = document.getElementById('deletion-overlay');

	function handleDelete(buttonClass, formClass, fetchUrl, extractDataCallback, rowSelectorPrefix) {
		const buttons = document.querySelectorAll(buttonClass);

		buttons.forEach(button => {
			button.addEventListener('click', () => {
				const form = button.closest(formClass);
				if (!form) return;

				const serviceId = form.getAttribute('data-id');
				console.log(`Ищем элемент с id: ${serviceId}`);

				if (!confirmDelete()) return;

				if (overlay) overlay.style.display = 'flex';

				const payload = extractDataCallback(form, serviceId);

				fetch(fetchUrl(serviceId), {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRFToken': getCookie('csrftoken')
					},
					body: JSON.stringify(payload)
				})
					.then(response => {
						if (overlay) overlay.style.display = 'none';
						if (!response.ok) throw new Error('Ошибка запроса');
						return response.json();
					})
					.then(data => {
						if (data.success || fetchUrl(serviceId).includes('delete_record_two')) {
							const row = document.querySelector(`${rowSelectorPrefix}[data-id="${serviceId}"]`);
							if (row) row.remove();
							alert('Элемент успешно удален!');
							window.location.reload();
						} else {
							alert('Ошибка: ' + JSON.stringify(data));
						}
					})
					.catch(error => {
						if (overlay) overlay.style.display = 'none';
						alert('У вас недостаточно прав для этого действия!');
						console.error('Ошибка:', error);
					});
			});
		});
	}

	handleDelete(
		'.delete-button',
		'.delete-form',
		() => '/delete_record/',
		(form, serviceId) => ({
			id: serviceId,
			page: form.getAttribute('data-page'),
			keyword_one: form.getAttribute('data-keyword-one'),
			keyword_two: form.getAttribute('data-keyword-two'),
			keyword_three: form.getAttribute('data-keyword-three'),
			keyword_four: form.getAttribute('data-keyword-four'),
			selected_column_one: form.getAttribute('data-selected-column-one'),
			selected_column_two: form.getAttribute('data-selected-column-two'),
			contract_date: form.getAttribute('data-contract-date'),
			selected_end_date: form.getAttribute('data-selected-end-date'),
			page_user: form.getAttribute('data-page-user'),
			page_user_two: form.getAttribute('data-page-user-two')
		}),
		'.service-row'
	);

	handleDelete(
		'.delete-button-user',
		'.delete-form-user',
		() => '/delete_record_two/',
		(form, serviceId) => ({
			id: serviceId,
			page: form.getAttribute('data-page'),
			keyword_one: form.getAttribute('data-keyword-one'),
			keyword_two: form.getAttribute('data-keyword-two'),
			keyword_three: form.getAttribute('data-keyword-three'),
			keyword_four: form.getAttribute('data-keyword-four'),
			selected_column_one: form.getAttribute('data-selected-column-one'),
			selected_column_two: form.getAttribute('data-selected-column-two'),
			contract_date: form.getAttribute('data-contract-date'),
			selected_end_date: form.getAttribute('data-selected-end-date'),
			page_user: form.getAttribute('data-page-user'),
			page_user_two: form.getAttribute('data-page-user-two')
		}),
		'.service-row-user'
	);
});