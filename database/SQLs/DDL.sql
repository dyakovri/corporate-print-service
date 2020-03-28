--------------------------------------------------------
-- DDL
--------------------------------------------------------
-- Отладка
drop schema if exists users, files, logs, automations cascade;

-- Работа с пользователями
create schema if not exists users;

drop table if exists users.type;
create table users.type(
    id serial primary key
, 	short_name varchar(64)
, 	description text
);
insert into users.type(id,short_name, description) values
(1,'superuser','User with administrator privileges, which can grants superusers.'),
(2,'admin','User with administrator privileges.'),
(3,'user::tradeunoun','User which can login with tradeunion number and surname.'),
(4,'user::student','User which can login with student number and surname.');


create table if not exists users.profile(
    id serial primary key
,	firstname varchar(64)
,	surname varchar(64)
,	middlename varchar(64)
, 	created timestamp default now()
, 	birthday date
, 	email varchar(256)
,	vkid integer
);

create table if not exists users.preregistred_profile(
    id serial primary key
,	firstname varchar(64)
,	surname varchar(64)
,	middlename varchar(64)
, 	birthday date
, 	email varchar(256)
, 	type_id integer
, 	login varchar(64)
, 	created timestamp default now()
,	expires timestamp
, 	foreign key (type_id) references users.type(id)
);

create table if not exists users.login(
    id serial primary key
,	user_id integer
,	type_id integer
, 	login varchar(64)
,	created timestamp default now()
, 	foreign key (user_id) references users.profile(id)
, 	foreign key (type_id) references users.type(id)
);

create table if not exists users.approval(
    id serial primary key
,   login_id integer
, 	binary_id integer --use lo_import and lo_export
, 	is_proved boolean
, 	created timestamp default now()
,	expires timestamp
, 	foreign key (login_id) references users.login(id)
);

-- Работа с файлами
create schema if not exists files;

drop table if exists files.type;
create table files.type(
    id serial primary key
, 	short_name varchar(64)
, 	description text
);
insert into files.type(id,short_name, description) values
(1,'pdf','Portable Document Format by Adobe');

create table if not exists files.file(
    id serial primary key
, 	pin integer
, 	user_id integer
, 	type_id integer
, 	hash varchar(32)
, 	size integer
,   page_count integer
, 	binary_id integer --use lo_import and lo_export
, 	created timestamp default now()
, 	foreign key (user_id) references users.profile(id)
, 	foreign key (type_id) references files.type(id)
);

create table if not exists files.file_option(
    id serial primary key
, 	file_id integer
, 	pages varchar(64)
,	count_per_list integer
, 	twosided boolean
, 	created timestamp default now()
, 	foreign key (file_id) references files.file(id)
);

--Работа с логом
create schema if not exists logs;

drop table if exists logs.type;
create table logs.type(
    id serial primary key
, 	short_name varchar(64)
, 	description text
);
insert into files.type(id,short_name, description) values
(100,'UserAction','Miscellaneous action with users'),
(101,'UserAddProfile','User add profile'),
(102,'UserAddLogin','User add login'),
(103,'UserDelete','User wipe'),
(104,'UserConfirm','User login confirmation by admin'),
(105,'UserAutoconfirm','User login confirmation by preregistred users'),
(106,'UserEdit','User parameters edit by admin'),
(200,'FileAction','Miscellaneous action with files'),
(201,'FileAdd','File uploaded by user'),
(202,'FileDelete','File deleted from server'),
(203,'FileOptionsAdd','File options added'),
(300,'VkbotAction','Miscellaneous action with VK bot'),
(301,'VkbotLogin','VK bot signed in'),
(302,'VkbotButtonClick','VK bot used'),
(400,'WebappAction','Miscellaneous action with Web app'),
(401,'WebappLogin','Web app signed in'),
(402,'WebappButtonClick','Web app used'),
(500,'TerminalappAction','Miscellaneous action with terminal app'),
(501,'TerminalappLogin','Terminal app signed in'),
(502,'TerminalappButtonClick','Terminal app used'),
(503,'TerminalappPrint','Terminal app sent document to printer');

create table if not exists logs.record(
    id serial primary key
, 	created timestamp default now()
, 	issuer_id integer
, 	user_id integer
, 	file_id integer
, 	type_id integer
, 	message text
--, 	foreign key (issuer_id) references pg_catalog.pg_user(usesysid)
, 	foreign key (user_id) references users.profile(id)
, 	foreign key (file_id) references files.file(id)
, 	foreign key (type_id) references logs.type(id)
);

-- Функции
create schema if not exists automations;

drop table if exists automations.response_code;
create table automations.response_code(
    id serial primary key
, 	short_name varchar(64)
, 	description text
);
-- Скопированы коды ответа HTTP, и так сойдет
insert into automations.response_code(id,short_name,description) values
-- Информационные
(100, 'Continue', '"Продолжить". Этот промежуточный ответ указывает, что запрос успешно принят и клиент может продолжать присылать запросы либо проигнорировать этот ответ, если запрос был завершён.'),
(101, 'Switching Protocol', '"Переключение протокола". Этот код присылается в ответ на запрос клиента, содержащий заголовок Upgrade:, и указывает, что сервер переключился на протокол, который был указан в заголовке. Эта возможность позволяет перейти на несовместимую версию протокола и обычно не используется.'),
(102, 'Processing', '"В обработке". Этот код указывает, что сервер получил запрос и обрабатывает его, но обработка еще не завершена.'),
(103, 'Early Hints', '"Ранние подсказки". В ответе сообщаются ресурсы, которые могут быть загружены заранее, пока сервер будет подготовливать основной ответ. RFC 8297 (Experimental).'),
-- Успешные
(200, 'OK', '"Успешно". Запрос успешно обработан. Что значит "успешно", зависит от метода, который был запрошен:'),
(201, 'Created', '"Создано". Запрос успешно выполнен и в результате был создан ресурс. Этот код обычно присылается в ответ на запрос PUT "ПОМЕСТИТЬ".'),
(202, 'Accepted', '"Принято". Запрос принят, но ещё не обработан. Не поддерживаемо, т.е., нет способа с помощью отправить асинхронный ответ позже, который будет показывать итог обработки запроса. Это предназначено для случаев, когда запрос обрабатывается другим процессом или сервером, либо для пакетной обработки.'),
(203, 'Non-Authoritative Information', '"Информация не авторитетна". Этот код ответа означает, что информация, которая возвращена, была предоставлена не от исходного сервера, а из какого-нибудь другого источника. Во всех остальных ситуациях более предпочтителен код ответа 200 OK.'),
(204, 'No Content', '"Нет содержимого". Нет содержимого для ответа на запрос, но заголовки ответа, которые могут быть полезны, присылаются. Клиент может использовать их для обновления кешированных заголовков полученных ранее для этого ресурса.'),
(205, 'Reset Content', '"Сбросить содержимое". Этот код присылается, когда запрос обработан, чтобы сообщить клиенту, что необходимо сбросить отображение документа, который прислал этот запрос.'),
(206, 'Partial Content', '"Частичное содержимое". Этот код ответа используется, когда клиент присылает заголовок диапазона, чтобы выполнить загрузку отдельно, в несколько потоков.'),
-- Перенаправления
(300, 'Multiple Choice', '"Множественный выбор". Этот код ответа присылается, когда запрос имеет более чем один из возможных ответов. И User-agent или пользователь должен выбрать один из ответов. Не существует стандартизированного способа выбора одного из полученных ответов.'),
(301, 'Moved Permanently', '"Перемещён на постоянной основе". Этот код ответа значит, что URI запрашиваемого ресурса был изменен. Возможно, новый URI будет предоставлен в ответе.'),
(302, 'Found', '"Найдено". Этот код ответа значит, что запрошенный ресурс временно изменен. Новые изменения в URI могут быть доступны в будущем. Таким образом, этот URI, должен быть использован клиентом в будущих запросах.'),
(303, 'See Other', '"Просмотр других ресурсов". Этот код ответа присылается, чтобы направлять клиента для получения запрашиваемого ресурса в другой URI с запросом GET.'),
(304, 'Not Modified', '"Не модифицировано". Используется для кэширования. Это код ответа значит, что запрошенный ресурс не был изменен. Таким образом, клиент может продолжать использовать кэшированную версию ответа.'),
(305, 'Use Proxy', '"Использовать прокси". Это означает, что запрошенный ресурс должен быть доступен через прокси. Этот код ответа в основном не поддерживается из соображений безопасности.'),
(306, 'Switch Proxy', 'Больше не использовать. Изначально подразумевалось, что " последующие запросы должны использовать указанный прокси."'),
(307, 'Temporary Redirect', '"Временное перенаправление". Сервер отправил этот ответ, чтобы клиент получил запрошенный ресурс на другой URL-адрес с тем же методом, который использовал предыдущий запрос. Данный код имеет ту же семантику, что код ответа 302 Found, за исключением того, что агент пользователя не должен изменять используемый метод: если в первом запросе использовался POST, то во втором запросе также должен использоваться POST.'),
(308, 'Permanent Redirect', '"Перенаправление на постоянной основе". Это означает, что ресурс теперь постоянно находится в другом URI, указанном в заголовке Location: Response. Данный код ответа имеет ту же семантику, что и код ответа 301 Moved Permanently, за исключением того, что агент пользователя не должен изменять используемый метод: если POST использовался в первом запросе, POST должен использоваться и во втором запросе.'),
-- Ошибки на стороне клиента
(400, 'Bad Request', '"Плохой запрос". Этот ответ означает, что сервер не понимает запрос из-за неверного синтаксиса. '),
(401, 'Unauthorized', '"Неавторизовано". Для получения запрашиваемого ответа нужна аутентификация. Статус похож на статус 403, но,в этом случае, аутентификация возможна. '),
(402, 'Payment Required', '"Необходима оплата". Этот код ответа зарезервирован для будущего использования. Первоначальная цель для создания этого когда была в использовании его для цифровых платежных систем(на данный момент не используется).'),
(403, 'Forbidden', '"Запрещено". У клиента нет прав доступа к содержимому, поэтому сервер отказывается дать надлежащий ответ. '),
(404, 'Not Found', '"Не найден". Сервер не может найти запрашиваемый ресурс. Код этого ответа, наверно, самый известный из-за частоты его появления в вебе. '),
(405, 'Method Not Allowed', '"Метод не разрешен". Сервер знает о запрашиваемом методе, но он был деактивирован и не может быть использован. Два обязательных метода,  GET и HEAD,  никогда не должны быть деактивированы и не должны возвращать этот код ошибки.'),
(406, 'Not Acceptable', 'Этот ответ отсылается, когда веб сервер после выполнения server-driven content negotiation, не нашел контента, отвечающего критериям, полученным из user agent.'),
(407, 'Proxy Authentication Required', 'Этот код ответа аналогичен коду 401, только аутентификация требуется для прокси сервера.'),
(408, 'Request Timeout', 'Ответ с таким кодом может прийти, даже без предшествующего запроса. Он означает, что сервер хотел бы отключить это неиспользуемое соеднинение. Этот метод используется все чаще с тех пор, как некоторые браузеры, вроде Chrome и IE9, стали использовать механизмы предварительного соединения для ускорения серфинга  (смотрите баг 881804, будущей реализации этого механизма в Firefox). Также учитывайте, что некоторые серверы прерывают соединения не отправляя подобных сообщений.'),
(409, 'Conflict', 'Этот ответ отсылается, когда запрос конфликтует с текущим состоянием сервера.'),
(410, 'Gone', 'Этот ответ отсылается, когда запрашиваемый контент удален с сервера.'),
(411, 'Length Required', 'Запрос отклонен, потому что сервер требует указание заголовка Content-Length, но он не указан.'),
(412, 'Precondition Failed', 'Клиент указал в своих заголовках условия, которые сервер не может выполнить'),
(413, 'Request Entity Too Large', 'Размер запроса превышает лимит, объявленный сервером. Сервер может закрыть соединение, вернув заголовок Retry-After'),
(414, 'Request-URI Too Long', 'URI запрашиваемый клиентом слишком длинный для того, чтобы сервер смог его обработать'),
(415, 'Unsupported Media Type', 'Медиа формат запрашиваемых данных не поддерживается сервером, поэтому запрос отклонен'),
(416, 'Requested Range Not Satisfiable', 'Диапозон указанный заголовком запроса Range не может быть выполнен; возможно, он выходит за пределы переданного URI'),
(417, 'Expectation Failed', 'Этот код ответа означает, что ожидание, полученное из заголовка запроса Expect, не может быть выполнено сервером.'),
-- Ошибки на стороне сервера
(500, 'Internal Server Error', '"Внутренняя ошибка сервера". Сервер столкнулся с ситуацией, которую он не знает как обработать. '),
(501, 'Not Implemented', '"Не выполнено". Метод запроса не поддерживается сервером и не может быть обработан. Единственные методы, которые сервера должны поддерживать (и, соответственно, не должны возвращать этот код) -  GET и HEAD.'),
(502, 'Bad Gateway', '"Плохой шлюз". Эта ошибка означает что сервер, во время работы в качестве шлюза для получения ответа, нужного для обработки запроса, получил недействительный (недопустимый) ответ. '),
(503, 'Service Unavailable', '"Сервис недоступен". Сервер не готов обрабатывать запрос. Зачастую причинами являются отключение сервера или то, что он перегружен. Обратите внимание, что вместе с этим ответом удобная для пользователей(user-friendly) страница должна отправлять объяснение проблемы.  Этот ответ должен использоваться для временных условий и Retry-After:-заголовок должен, если возможно, содержать  предполагаемое время до восстановления сервиса. Веб-мастер также должен позаботиться о заголовках, связанных с кэшем, которые отправляются вместе с этим ответом, так как эти ответы, связанные с временными условиями, обычно не должны кэшироваться. '),
(504, 'Gateway Timeout', 'Этот ответ об ошибке предоставляется, когда сервер действует как шлюз и не может получить ответ вовремя.'),
(505, ' Version Not Supported', '"версия не поддерживается". Версия, используемая в запроcе, не поддерживается сервером.');