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

function updateFileName() {
	const fileInput = document.getElementById('file-input');
	const fileNameDisplay = document.getElementById('file-name');
	const submitButton = document.getElementById('submit-button');

	if (fileInput.files.length > 0) {
		const fileName = fileInput.files[0].name;
		fileNameDisplay.textContent = `Выбран файл: ${fileName}`;

		Object.assign(fileNameDisplay.style, {
			display: 'inline-block',
			verticalAlign: 'middle',
			border: '2px solid red',
			padding: '8px 12px',
			borderRadius: '5px',
			margin: '0 10px 20px 10px'
		});

		submitButton.style.display = 'inline';
	} else {
		fileNameDisplay.textContent = '';

		Object.assign(fileNameDisplay.style, {
			display: '',
			verticalAlign: '',
			border: '',
			padding: '',
			borderRadius: '',
			margin: ''
		});

		submitButton.style.display = 'none';
	}
}

function showFlashMessage(event) {
	event.preventDefault();

	const fileInput = document.getElementById("file-input");
	const submitButton = document.getElementById("submit-button");
	const message = document.getElementById("flash-message-import");
	const overlay = document.getElementById('deletion-overlay');
	const fileNameDisplay = document.getElementById('file-name');

	if (fileInput.files.length === 0) {
		alert("Выберите файл перед отправкой!");
		return;
	}

	// Вспомогательные функции
	const toggleLoading = (isLoading) => {
		submitButton.style.display = isLoading ? 'none' : 'inline-block';
		if (overlay) overlay.style.display = isLoading ? 'flex' : 'none';
		document.body.style.overflow = isLoading ? 'hidden' : '';
	};

	const resetFileNameDisplay = () => {
		fileNameDisplay.textContent = '';
		Object.assign(fileNameDisplay.style, {
			display: '',
			verticalAlign: '',
			border: '',
			padding: '',
			borderRadius: '',
			margin: ''
		});
	};

	const showMessage = (text, isSuccess) => {
		message.textContent = text;
		message.classList.remove("alert-success", "alert-danger");
		message.classList.add(isSuccess ? "alert-success" : "alert-danger");
		message.style.display = "block";
	};

	toggleLoading(true);

	const formData = new FormData();
	formData.append("file", fileInput.files[0]);

	fetch("/upload/", {
		method: "POST",
		body: formData,
		headers: {
			"X-CSRFToken": getCookie("csrftoken")
		}
	})
		.then(response => response.json())
		.then(data => {
			toggleLoading(false);
			showMessage(data.message || "Ответ без сообщения от сервера", data.status === "success");

			if (data.success) {
				setTimeout(() => {
					window.location.reload();
				}, 2000);
			} else {
				resetFileNameDisplay();
				submitButton.style.display = 'none';
				console.error("Ошибка сервера:", data);
			}
		})
		.catch(error => {
			toggleLoading(false);
			showMessage("У вас недостаточно прав для этого действия!", false);

			resetFileNameDisplay();
			submitButton.style.display = 'none';

			console.error("Ошибка загрузки файла:", error);
		});
}

// Универсальная функция сброса фильтров и прокрутки
function resetFiltersGeneric({ pageParam, totalPagesParam, filters = [] }) {
	// Сохраняем текущую позицию прокрутки
	sessionStorage.setItem('scrollPosition', window.scrollY);

	// Получаем текущую страницу
	const currentPage = new URLSearchParams(window.location.search).get(pageParam) || 1;

	// Формируем URL с параметрами GET
	const url = new URL(window.location.href);

	// Устанавливаем переданные фильтры
	for (const { key, value } of filters) {
		url.searchParams.set(key, value);
	}

	// Устанавливаем параметр страницы
	url.searchParams.set(totalPagesParam, currentPage);

	// Перезагружаем страницу с обновлёнными параметрами
	window.location.href = url;
}

// Специализированные обёртки:

function resetFilters() {
	resetFiltersGeneric({
		pageParam: 'page',
		totalPagesParam: 'total_pages_full',
		filters: [
			{ key: 'contract_date', value: 'No' },
			{ key: 'end_date', value: 'No' },
			{ key: 'keyword_one', value: '' },
			{ key: 'keyword_two', value: '' },
			{ key: 'keyword_three', value: '' },
			{ key: 'keyword_four', value: '' },
			{ key: 'selected_column_one', value: '' },
			{ key: 'selected_column_two', value: '' },
			{ key: 'selected_column_three', value: '' },
			{ key: 'selected_column_four', value: '' }
		]
	});
}

function resetFiltersUser() {
	resetFiltersGeneric({
		pageParam: 'page_user',
		totalPagesParam: 'total_pages_full_user',
		// Можно раскомментировать и добавить фильтры при необходимости
		// filters: [
		// 	{ key: 'KOSGU_user', value: 'No' },
		// 	{ key: 'keyword_one_user', value: '' },
		// 	{ key: 'keyword_two_user', value: '' },
		// 	{ key: 'selected_column_one_user', value: '' },
		// 	{ key: 'selected_column_two_user', value: '' }
		// ]
	});
}

function resetFiltersUserTwo() {
	resetFiltersGeneric({
		pageParam: 'page_user_two',
		totalPagesParam: 'total_pages_full_user_two',
		// Можно раскомментировать и добавить фильтры при необходимости
		// filters: [
		// 	{ key: 'KOSGU_user_two', value: 'No' },
		// 	{ key: 'keyword_one_user_two', value: '' },
		// 	{ key: 'keyword_two_user_two', value: '' },
		// 	{ key: 'selected_column_one_user_two', value: '' },
		// 	{ key: 'selected_column_two_user_two', value: '' }
		// ]
	});
}

// Универсальная функция обновления цвета строки
function updateRowColor(endpoint, rowSelector, rowId, color) {
	console.log('data');
	fetch(`${endpoint}${rowId}/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCookie('csrftoken')
		},
		body: JSON.stringify({ color: color })
	})
		.then(response => response.json())
		.then(data => {
			console.log(data);
			if (data.success) {
				const row = document.querySelector(`${rowSelector}[data-id="${data.id}"]`);
				if (row) {
					row.style.backgroundColor = data.color;
					const cells = row.querySelectorAll('td');
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
			console.error('Ошибка:', error);
		});
}

// Обёртки для конкретных случаев
function updateColor(rowId, color) {
	updateRowColor('/update_color/', '.service-row', rowId, color);
}

function updateColorUser(rowId, color) {
	updateRowColor('/update_color_user/', '.service-row-user', rowId, color);
}

function updateColorUserTwo(rowId, color) {
	updateRowColor('/update_color_user_two/', '.service-row-user-two', rowId, color);
}

function confirmDelete() {
	return confirm('Вы уверены, что хотите удалить этот элемент?');
}

// window.addEventListener('beforeunload', function () {
// 	// Сохранение позиции скролла
// 	localStorage.setItem('scrollPosition', window.scrollY);
// });

// Функция для установки обработчика сброса фильтров
function addResetHandler(buttonId, resetFunction) {
	const button = document.getElementById(buttonId);
	if (button) {
		button.addEventListener('click', resetFunction);
	}
}

// Добавляем обработчики на кнопки сброса
addResetHandler('reset-filters', resetFilters);
addResetHandler('reset-filters-user', resetFiltersUser);
addResetHandler('reset-filters-user-two', resetFiltersUserTwo);

// Функция для установки обработчика сохранения позиции прокрутки
function addScrollSaveOnSubmit(formId) {
	const form = document.getElementById(formId);
	if (form) {
		form.addEventListener('submit', () => {
			sessionStorage.setItem('scrollPosition', window.scrollY);
		});
	}
}

// Добавляем обработчики на формы
['filter-form', 'filter-form-user', 'filter-form-user-two'].forEach(addScrollSaveOnSubmit);

document.addEventListener("DOMContentLoaded", function () {

	// Прокрутка страницы по scroll_position из URL при загрузке
	const urlParams = new URLSearchParams(window.location.search);
	const scrollPos = urlParams.get('scroll_position');

	if (scrollPos !== null && !isNaN(parseInt(scrollPos, 10))) {
		// Если есть scroll_position в URL — прокрутить по нему
		window.scrollTo({
			top: parseInt(scrollPos, 10),
			behavior: 'instant' // можно 'smooth', если нужно плавно
		});
	} else {
		// Если scroll_position нет — пытаемся восстановить из sessionStorage
		const savedPos = sessionStorage.getItem('scrollPosition');
		if (savedPos !== null && !isNaN(parseInt(savedPos, 10))) {
			window.scrollTo(0, parseInt(savedPos, 10));
			sessionStorage.removeItem('scrollPosition');
		}
	}

	// Обработчик для ссылок с классом .edit-link
	document.querySelectorAll('.edit-link').forEach(function (link) {
		link.addEventListener('click', function (event) {
			// Получаем текущую позицию скролла
			const currentScroll = window.scrollY || document.documentElement.scrollTop;

			// Добавляем/обновляем параметр scroll_position в href
			const url = new URL(link.href, window.location.origin);
			url.searchParams.set('scroll_position', currentScroll);

			// Обновляем ссылку
			link.href = url.toString();
		});
	});

	const exportButton = document.getElementById("export-button");
	const message = document.getElementById("flash-message-export");
	const form = document.getElementById("export-form");

	let requestInProgress = false;
	let taskId = null;
	let checkStatusInterval = null;

	function showMessage(text, type = "success") {
		message.textContent = text;
		message.className = ""; // Сброс классов
		message.classList.add("alert", `alert-${type}`);
		message.style.display = "block";
	}

	function handleExportStart(data) {
		taskId = data.task_id;
		console.log(`Экспорт начат, ID задачи: ${taskId}`);

		checkStatusInterval = setInterval(() => {
			console.log(`Проверка статуса задачи с ID: ${taskId}`);
			socket.send(JSON.stringify({ action: "check_task_status", task_id: taskId }));
		}, 2000);
	}

	function handleExportSuccess(data) {
		console.log(`Экспорт завершён успешно: ${data.filename}`);
		clearInterval(checkStatusInterval);

		const link = document.createElement("a");
		link.href = data.file_url;
		link.download = data.filename;
		link.click();

		showMessage("Экспорт завершен!", "success");
		requestInProgress = false;
	}

	function handleExportError(data) {
		console.log("Произошла ошибка формирования файла:", data.message);
		showMessage(`Произошла ошибка формирования файла: ${data.message}`, "danger");
		requestInProgress = false;
	}

	function handleTaskPending() {
		console.log("Ожидание выполнения... Файл очень большой.");
		showMessage("В ожидании... Очень большой объём файла!", "success");
	}

	function handleTaskFailure(data) {
		console.log("Ошибка экспорта:", data.error);
		showMessage(`Ошибка экспорта! ${data.error}`, "danger");
		requestInProgress = false;
		clearInterval(checkStatusInterval);
	}

	function handleDisconnect() {
		console.log("Соединение потеряно. Экспорт отменён!");
		showMessage("Соединение потеряно. Экспорт отменён!", "danger");
		requestInProgress = false;
		clearInterval(checkStatusInterval);
	}

	exportButton.onclick = function (event) {
		event.preventDefault();

		if (requestInProgress) {
			console.log("Запрос уже выполняется, новая отправка отменена");
			return;
		}

		if (!form) {
			console.error("Ошибка: форма не найдена!", form);
			return;
		}

		const formData = new FormData(form);
		const contract_date = formData.get("contract_date");
		const end_date = formData.get("end_date");

		console.log(`Отправка запроса на экспорт для года: ${contract_date} и ${end_date}`);

		requestInProgress = true;
		showMessage("Пожалуйста, подождите, идёт загрузка!", "success");

		socket.send(
			JSON.stringify({
				action: "export_excel",
				contract_date,
				end_date,
			})
		);
	};

	socket.onmessage = function (event) {
		const data = JSON.parse(event.data);

		switch (data.type) {
			case "export_started":
				handleExportStart(data);
				break;

			case "export_success":
				handleExportSuccess(data);
				break;

			case "export_error":
				handleExportError(data);
				break;

			case "task_status_pending":
				handleTaskPending();
				break;

			case "task_status_failure":
				handleTaskFailure(data);
				break;

			case "disconnect":
				handleDisconnect();
				break;

			default:
				console.warn("Неизвестный тип сообщения:", data.type);
		}
	};

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

	document.querySelectorAll('.text-content').forEach(textContent => {
		const button = textContent.nextElementSibling;

		const isOverflowing = textContent.scrollHeight > textContent.clientHeight;
		button.style.display = isOverflowing ? 'block' : 'none';

		button.addEventListener('click', () => {
			textContent.classList.toggle('expanded');
			button.textContent = textContent.classList.contains('expanded') ? 'Скрыть' : 'Показать больше';
		});
	});

	function setupBackupButton(buttonId, messageId, confirmText) {
		const button = document.getElementById(buttonId);
		const overlay = document.getElementById('deletion-overlay');
		if (!button) return;

		button.addEventListener('click', function (e) {
			e.preventDefault();

			if (!confirm(confirmText)) return;

			const url = button.getAttribute('data-url');
			const flashMessage = document.getElementById(messageId);

			console.log('URL для fetch:', url);

			if (overlay) overlay.style.display = 'flex';
			document.body.style.overflow = 'hidden'; // блокируем скролл

			fetch(url, { method: 'GET' })
				.then(response => {
					console.log('RAW response:', response);
					return response.json();
				})
				.then(data => {
					if (overlay) overlay.style.display = 'none';
					document.body.style.overflow = ''; // восстанавливаем скролл

					flashMessage.textContent = data.success ? 'Удачно!' : (data.message || 'Произошла ошибка!');
					flashMessage.style.display = 'block';
					flashMessage.classList.toggle('alert-success', data.success);
					flashMessage.classList.toggle('alert-danger', !data.success);

					// Дай пользователю 1–2 секунды увидеть сообщение перед перезагрузкой
					setTimeout(() => {
						window.scrollTo(0, 0);
						window.location.reload();
					}, 2000);
				})
				.catch(error => {
					if (overlay) overlay.style.display = 'none';
					document.body.style.overflow = ''; // восстанавливаем скролл

					flashMessage.textContent = 'У вас недостаточно прав для этого действия!';
					flashMessage.style.display = 'block';
					flashMessage.classList.remove('alert-success');
					flashMessage.classList.add('alert-danger');
				});
		});
	}

	// Инициализация обработчиков
	setupBackupButton('backup-one-button', 'flash-message-one', 'Вы уверены, что хотите выполнить резервное копирование для вторника?');
	setupBackupButton('backup-two-button', 'flash-message-two', 'Вы уверены, что хотите выполнить резервное копирование для четверга?');

	const configs = [
		{ selector: '.color-select', handler: updateColor },
		{ selector: '.color-select-user', handler: updateColorUser },
		{ selector: '.color-select-user-two', handler: updateColorUserTwo },
	];

	configs.forEach(({ selector, handler }) => {
		const colorSelects = document.querySelectorAll(selector);

		colorSelects.forEach(select => {
			select.addEventListener('change', function () {
				const rowId = this.getAttribute('data-id');
				const selectedColor = this.value;

				handler(rowId, selectedColor);
			});
		});
	});

	if (!navigator.userAgent.includes('AppleWebKit')) {
		// document.querySelector('.wrapper').innerHTML = '<p>Sorry! Non webkit users.</p>';
		console.log('Sorry! Non webkit users!');
	}

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
				document.body.style.overflow = 'hidden'; // блокируем скролл

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
						document.body.style.overflow = ''; // восстанавливаем скролл
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
						document.body.style.overflow = ''; // восстанавливаем скролл
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

	const colors = ["#4F83CC", "green"];
	let index = 0;

	document.querySelectorAll("#myTable tbody tr").forEach(tr => {
		const color = colors[index % colors.length]; // выбираем цвет по очереди
		index++;
		tr.querySelectorAll("td").forEach(td => {
			td.style.borderBottom = "2px solid " + color; // только нижняя рамка
		});
	});

});