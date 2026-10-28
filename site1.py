from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

# СЕКРЕТНЫЙ КОНТУР БЕЗОПАСНОСТИ (Пароль для управления сайтом)
ADMIN_PASSWORD = "admin68"

# 1. РЕАЛЬНАЯ БАЗА ЗВОНКОВ ПО ТВОЕЙ ТАБЛИЦЕ (Школа №25 и Интернат №32)
INTERNAT_BELLS = [
    {"num": "1 смена - 1 урок", "time": "08:30 - 09:10"},
    {"num": "1 смена - 2 урок", "time": "09:30 - 10:10"},
    {"num": "1 смена - 3 урок", "time": "10:30 - 11:10"},
    {"num": "1 смена - 4 урок", "time": "11:30 - 12:10"},
    {"num": "1 смена - 5 урок", "time": "12:20 - 13:00"},
    {"num": "1 смена - 6 урок", "time": "13:20 - 14:00"},
    {"num": "2 смена - 1 урок", "time": "14:10 - 14:50"},
    {"num": "2 смена - 2 урок", "time": "15:10 - 15:50"},
    {"num": "2 смена - 3 урок", "time": "16:00 - 16:40"},
    {"num": "2 смена - 4 урок", "time": "16:50 - 17:30"},
    {"num": "2 смена - 5 урок", "time": "17:40 - 18:20"},
    {"num": "2 смена - 6 урок", "time": "18:30 - 19:10"}
]

SCHOOL_25_BELLS = [
    {"num": "1 смена - 1 урок", "time": "08:00 - 08:40"},
    {"num": "1 смена - 2 урок", "time": "08:50 - 09:30"},
    {"num": "1 смена - 3 урок", "time": "09:45 - 10:25"},
    {"num": "1 смена - 4 урок", "time": "10:35 - 11:15"},
    {"num": "1 смена - 5 урок", "time": "11:25 - 12:05"},
    {"num": "1 смена - 6 урок", "time": "12:10 - 12:50"},
    {"num": "2 смена - 1 урок", "time": "13:05 - 13:45"},
    {"num": "2 смена - 2 (1) урок", "time": "14:00 - 14:40"},
    {"num": "2 смена - 3 (2) урок", "time": "14:50 - 15:30"},
    {"num": "2 смена - 4 (3) урок", "time": "15:40 - 16:20"},
    {"num": "2 смена - 5 (4) урок", "time": "16:25 - 17:05"},
    {"num": "2 смена - 6 (5) урок", "time": "17:10 - 17:50"},
    {"num": "2 смена - 7 (6) урок", "time": "17:55 - 18:35"}
]

def get_db():
    conn = sqlite3.connect("school68.db")
    conn.row_factory = sqlite3.Row
    return conn

with get_db() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, text TEXT, image TEXT)")
    conn.execute("INSERT OR IGNORE INTO settings VALUES ('schedule', 'https://unsplash.com')")
    conn.execute("INSERT OR IGNORE INTO settings VALUES ('main_schedule', 'https://unsplash.com')")
    conn.commit()

# СТИЛИСТИЧЕСКИЙ КАРКАС (Дорогой неоновый Cyber-дизайн)
STYLE = '''
<style>
    body { background-color: #0f111a; color: #c3c7db; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }
    .container { max-width: 1050px; margin: 40px auto; padding: 20px; }
    .header { text-align: center; border-bottom: 2px solid #1f2335; padding-bottom: 20px; margin-bottom: 30px; }
    .header h1 { color: #41a5f5; font-size: 2.5rem; text-shadow: 0 0 10px rgba(65, 165, 245, 0.3); margin: 0 0 10px 0; }
    .nav-menu { display: flex; justify-content: center; flex-wrap: wrap; gap: 15px; margin-bottom: 30px; }
    .nav-link { color: #7aa2f7; text-decoration: none; font-weight: bold; padding: 10px 20px; border: 1px solid #2e3c64; border-radius: 8px; transition: all 0.3s ease; background: #1a1b26; }
    .nav-link:hover { color: #fff; border-color: #7aa2f7; box-shadow: 0 0 15px rgba(122, 162, 247, 0.4); transform: translateY(-2px); }
    .card { background: #1a1b26; border: 1px solid #24283b; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
    .card h3 { color: #2ac3de; margin-top: 0; font-size: 1.3rem; border-bottom: 1px solid #24283b; padding-bottom: 8px; margin-bottom: 15px; }
    .btn { background: #41a5f5; color: #fff; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: all 0.3s ease; text-decoration: none; display: inline-block; }
    .btn:hover { background: #7aa2f7; box-shadow: 0 0 15px rgba(122, 162, 247, 0.5); }
.btn-danger { background: #f7768e; padding: 6px 12px; font-size: 0.85rem; border-radius: 6px; margin-top: 10px; }
    .btn-danger:hover { background: #ff0055; box-shadow: 0 0 10px rgba(247, 118, 142, 0.5); }
    .form-control { width: 100%; padding: 12px; background: #15161e; border: 1px solid #24283b; border-radius: 8px; color: #fff; font-size: 1rem; box-sizing: border-box; margin-bottom: 15px; }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .teacher-row { display: flex; align-items: center; gap: 15px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #1f2335; }
    .cyber-avatar { width: 45px; height: 45px; border-radius: 50%; background: #15161e; border: 2px solid #7aa2f7; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #7aa2f7; font-size: 0.85rem; text-shadow: 0 0 8px rgba(122, 162, 247, 0.6); }
    .fipi-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 15px; }
    .fipi-box { background: #15161e; padding: 15px; border-radius: 8px; border: 1px solid #24283b; }
    .fipi-link { display: inline-block; margin-top: 5px; color: #bb9af3; text-decoration: none; font-weight: bold; border-bottom: 1px dashed #bb9af3; transition: all 0.3s ease; }
    .fipi-link:hover { color: #fff; border-bottom-color: #fff; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 15px; }
    th, td { border: 1px solid #24283b; padding: 8px; text-align: left; font-size: 0.9rem; }
    th { background: #15161e; color: #2ac3de; }
    ul { padding-left: 20px; line-height: 1.8; color: #a9b1d6; }
</style>
'''

@app.route('/')
def home():
    conn = get_db()
    current_schedule_photo = conn.execute("SELECT value FROM settings WHERE key='schedule'").fetchone()['value']
    current_main_schedule_photo = conn.execute("SELECT value FROM settings WHERE key='main_schedule'").fetchone()['value']
    news_list = conn.execute("SELECT * FROM news ORDER BY id DESC").fetchall()
    conn.close()
    html = f'''
    <html><head>{STYLE}</head><body>
        <div class="container">
            <div class="header">
                <h1>Средняя общеобразовательная школа №68</h1>
                <p style="color: #565f89;">Цифровая инфраструктура образовательного учреждения в период реновации основного здания</p>
            </div>
            <div class="nav-menu">
                <a href="/" class="nav-link">Главная</a>
                <a href="/schedule" class="nav-link">Расписание и звонки</a>
                <a href="/teachers" class="nav-link">Педагогический состав</a>
                <a href="/exam" class="nav-link">Мониторинг знаний ГИА (ФИПИ)</a>
            </div>
            <div class="grid-2">
                <div>
                    <h2>Лента официальных пресс-релизов:</h2>
                    {{% for news in news_list %}}
                        <div class="card">
                            <h3 style="color: #41a5f5;">{{{{ news.title }}}}</h3>
                            <p style="line-height: 1.6; color: #a9b1d6;">{{{{ news.text|safe }}}}</p>
                            {{% if news.image %}}
                                <img src="{{{{ news.image }}}}" alt="Иллюстрация" style="width: 100%; border-radius: 8px; border: 1px solid #24283b; margin-top: 12px;">
                            {{% endif %}}
                            
                        </div>
                    {{% endfor %}}
                </div>
                <div>
                    <h2>Оперативные изменения в расписании:</h2>
                    <div class="card" style="border-color: #73daca; text-align: center;">
                        <h3 style="color: #73daca;">Текущий бланк замен на сегодня</h3>
                        {{% if current_schedule_photo and "unsplash.com" not in current_schedule_photo %}}
                            <img src="{{{{ current_schedule_photo }}}}" alt="Бланк замен" style="width: 100%; border-radius: 8px; border: 1px solid #24283b; margin-top: 10px;">
                        {{% else %}}
                            <div style="background: #15161e; border: 1px dashed #24283b; padding: 30px; border-radius: 8px; color: #565f89; font-size: 0.95rem; margin-top: 15px;">
                                📁  Официальный бланк замен на сегодня не загружен.<br>
                                <span style="color: #73daca; font-size: 0.85rem;">Занятия проводятся в штатном режиме по постоянному расписанию.</span>
                            </div>
                        {{% endif %}}
                        <p style="color: #565f89; font-size: 0.85rem; margin-top: 15px;">* Изменения публикуются диспетчером через Панель управления</p>
                    </div>
                    </div>
                </div>
            </div>
        </body></html>
        '''
    return render_template_string(html, news_list=news_list, current_schedule_photo=current_schedule_photo)


@app.route('/schedule')
def schedule():
    conn = get_db()
    current_main_schedule_photo = conn.execute("SELECT value FROM settings WHERE key='main_schedule'").fetchone()[
        'value']
    conn.close()
    html = f'''
        <html><head>{STYLE}</head><body>
            <div class="container">
                <div class="header">
                    <h1>График и расписание занятий МБОУ СОШ №68</h1>
                    <p style="color: #ff9e64;">Временный регламент работы на период реновации (Распределение по школам)</p>
                </div>
                <div class="nav-menu"><a href="/" class="nav-link">Назад на главную</a></div>

                <div class="grid-2">
                    <!-- КОРПУС ШКОЛЫ №25 (6-11 КЛАССЫ) -->
                    <div class="card" style="border-color: #41a5f5;">
                        <h3 style="color: #41a5f5;">База обучения: Школа №25 (6-11 классы)</h3>
                        <p style="font-size:0.9rem; color:#a9b1d6; margin-bottom:10px;">
                            <strong>1 смена (08:00):</strong> Все 9, 10, 11 классы (включая единственные 10-й и 11-й монолит-классы).<br>
                            <strong>2 смена (13:05):</strong> 6, 7 классы, параллели 8А и 8В, а также <strong>8Б класс</strong> (обучается во 2-ю смену обособленно от параллели).
                        </p>
                        <h4 style="color:#2ac3de; margin-bottom:5px;">Сетка звонков (Школа №25):</h4>
                        <table>
                            <tr><th>Урок</th><th>Интервал</th></tr>
                            {{% for bell in school_bells %}}
                            <tr><td><strong>{{{{ bell.num }}}}</strong></td><td style="color:#73daca;">{{{{ bell.time }}}}</td></tr>
                            {{% endfor %}}
                        </table>
                    </div>

                    <!-- КОРПУС ИНТЕРНАТА №32 (1-5 КЛАССЫ) -->
                    <div class="card" style="border-color: #bb9af3;">
                        <h3 style="color: #bb9af3;">База обучения: Интернат №32 (1-5 классы)</h3>
                        <p style="font-size:0.9rem; color:#a9b1d6; margin-bottom:10px;">
                            <strong>1 смена (08:30):</strong> Все 5 классы, а также начальные классы: 1А, 1Б, 4А.<br>
                            <strong>2 смена (14:10):</strong> Начальные классы: 2А, 2Б, 3А, 3Б, 4Б.
                        </p>
                        <h4 style="color:#2ac3de; margin-bottom:5px;">Сетка звонков строго по бланку (Интернат):</h4>
                        <table>
                            <tr><th>Урок</th><th>Интервал</th></tr>
                            {{% for bell in internat_bells %}}
                            <tr><td><strong>{{{{ bell.num }}}}</strong></td><td style="color:#73daca;">{{{{ bell.time }}}}</td></tr>
                            {{% endfor %}}
                        </table>
                    </div>
                </div>

                <!-- ПОСТОЯННОЕ ОСНОВНОЕ РАСПИСАНИЕ УРОКОВ -->
                <div class="card" style="border-color: #73daca; text-align: center;">
                    <h3 style="color: #73daca;">Основное стабильное расписание уроков</h3>
                    <img src="{{{{ main_schedule_photo }}}}" alt="Основное расписание" style="width: 100%; max-width:850px; border-radius: 8px; border: 1px solid #24283b; margin-top: 10px;">
                    <p style="color: #565f89; font-size: 0.85rem; margin-top: 10px;"> </p>
                </div>
            </div>
        </body></html>
        '''
    return render_template_string(html, school_bells=SCHOOL_25_BELLS, internat_bells=INTERNAT_BELLS,
                                  main_schedule_photo=current_main_schedule_photo)


@app.route('/teachers')
def teachers():
    html = f'''
    <html><head>{STYLE}</head><body>
        <div class="container">
            <div class="header"><h1>Педагогический коллектив МБОУ СОШ №68</h1></div>
            <div class="nav-menu"><a href="/" class="nav-link">Назад на главную</a></div>

            <div class="card">
                <h3>Административный состав и специалисты учебной части</h3>
                <div class="teacher-row"><div class="cyber-avatar">СЕК</div><div><strong>Селезнёва Арина Сергеевна</strong><br><span style="color: #565f89;">Секретарь учебной части</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">БИБ</div><div><strong>Зайцева Наталья Олеговна</strong><br><span style="color: #565f89;">Педагог-библиотекарь</span></div></div>
            </div>

            <div class="card">
                <h3>Кафедра точных и естественных наук</h3>
                <div class="teacher-row"><div class="cyber-avatar">МАТ</div><div><strong>Суртаева Вера Ивановна</strong><br><span style="color: #565f89;">Учитель математики</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">МАТ</div><div><strong>Хакимова Анна Александровна</strong><br><span style="color: #565f89;">Учитель математики</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">МАТ</div><div><strong>Старченко Елизавета Владимировна</strong><br><span style="color: #565f89;">Учитель математики • Старшая вожатая</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">ИНФ</div><div><strong>Старченко Вадим Вячеславович</strong><br><span style="color: #565f89;">Учитель информатики и ИКТ</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">ФИЗ</div><div><strong>Руднева Елена Николаевна</strong><br><span style="color: #565f89;">Учитель физики</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">БИО</div><div><strong>Балде Ольга Александровна</strong><br><span style="color: #565f89;">Учитель биологии</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">ХИМ</div><div><strong>Суковицина Дарья Андреевна</strong><br><span style="color: #565f89;">Учитель химии</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">ГЕО</div><div><strong>Печурина Виктория Сергеевна</strong><br><span style="color: #565f89;">Учитель географии</span></div></div>
            </div>

            <div class="card">
                <h3>Кафедра гуманитарных и общественных дисциплин</h3>
                <div class="teacher-row"><div class="cyber-avatar">РУС</div><div><strong>Каменева Елена Авенировна</strong><br><span style="color: #565f89;">Учитель русского языка и литературы</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">РУС</div><div><strong>Тарасова Елена Витальевна</strong><br><span style="color: #565f89;">Учитель русского языка и литературы</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">РУС</div><div><strong>Черникова Алина Рафисовна</strong><br><span style="color: #565f89;">Учитель русского языка и литературы</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">РУС</div><div><strong>Соболева Лилия Валерьевна</strong><br><span style="color: #565f89;">Учитель русского языка и литературы</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">ИСТ</div><div><strong>Хузина Екатерина Владимировна</strong><br><span style="color: #565f89;">Учитель истории и обществознания</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">АНГ</div><div><strong>Бурмашова Оксана Викторовна</strong><br><span style="color: #565f89;">Учитель английского языка</span></div></div>
<div class="teacher-row"><div class="cyber-avatar">АНГ</div><div><strong>Штанговец Татьяна Сергеевна</strong><br><span style="color: #565f89;">Учитель английского языка</span></div></div>
            </div>

            <div class="card">
                <h3>Методическое объединение начальных классов</h3>
                <div class="teacher-row"><div class="cyber-avatar">НАЧ</div><div><strong>Иванютина Ольга Викторовна</strong><br><span style="color: #565f89;">Учитель начальных классов • Руководитель МО</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">НАЧ</div><div><strong>Баранникова Татьяна Валерьевна</strong><br><span style="color: #565f89;">Учитель начальных классов</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">НАЧ</div><div><strong>Земцова Ирина Николаевна</strong><br><span style="color: #565f89;">Учитель начальных классов</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">НАЧ</div><div><strong>Ощепкова Любовь Валериевна</strong><br><span style="color: #565f89;">Учитель начальных классов</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">НАЧ</div><div><strong>Кузнецова Татьяна Сергеевна</strong><br><span style="color: #565f89;">Учитель начальных классов</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">НАЧ</div><div><strong>Барыкина Юлия Геннадьевна</strong><br><span style="color: #565f89;">Учитель начальных классов</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">НАЧ</div><div><strong>Сафонова Наталья Анатольевна</strong><br><span style="color: #565f89;">Учитель начальных классов</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">НАЧ</div><div><strong>Солдатова Татьяна Владимировна</strong><br><span style="color: #565f89;">Учитель начальных классов</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">НАЧ</div><div><strong>Лисиенко Ирина Анатольевна</strong><br><span style="color: #565f89;">Учитель начальных классов</span></div></div>
            </div>

            <div class="card">
                <h3>Кафедра прикладных дисциплин и физической культуры</h3>
                <div class="teacher-row"><div class="cyber-avatar">ФИЗ</div><div><strong>Смольникова Людмила Анатольевна</strong><br><span style="color: #565f89;">Учитель физической культуры</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">ФИЗ</div><div><strong>Нефедова Вера Анатольевна</strong><br><span style="color: #565f89;">Учитель физической культуры</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">ФИЗ</div><div><strong>Пашкевич Евгений Викторович</strong><br><span style="color: #565f89;">Учитель физической культуры</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">ТРД</div><div><strong>Кемерова Ирина Николаевна</strong><br><span style="color: #565f89;">Учитель труда (технологии)</span></div></div>
                <div class="teacher-row"><div class="cyber-avatar">ИЗО</div><div><strong>Чернова Надежда Викторовна</strong><br><span style="color: #565f89;">Учитель изобразительного искусства</span></div></div>
            </div>
        </div>
    </body></html>
    '''
    return render_template_string(html)


@app.route('/exam')
def exam():
    html = f'''
        <html><head>{STYLE}</head><body>
            <div class="container">
                <div class="header"><h1>Интерактивный модуль мониторинга знаний ГИА</h1></div>
                <div class="nav-menu"><a href="/" class="nav-link">Назад на главную</a></div>

                <div class="card">
                    <h3>Единый Государственный Экзамен (РАЗДЕЛ ЕГЭ)</h3>
    <p style="color: #a9b1d6;">Прямые калиброванные шлюзы к предметным интерактивным базам ФИПИ без ошибок:</p>
                    <div class="fipi-grid">
                        <div class="fipi-box"><h4>Математика (Профиль)</h4><a href="https://ege.fipi.ru/bank/index.php?proj=AC437B34557F88EA4115D2F374B0A07B" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Математика (База)</h4><a href="https://ege.fipi.ru/bank/index.php?proj=E040A72A1A3DABA14C90C97E0B6EE7DC" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Информатика и ИКТ</h4><a href="https://ege.fipi.ru/bank/index.php?proj=B9ACA5BBB2E19E434CD6BEC25284C67F" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Биология</h4><a href="https://ege.fipi.ru/bank/index.php?proj=CA9D848A31849ED149D382C32A7A2BE4" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>География</h4><a href="https://ege.fipi.ru/bank/index.php?proj=20E79180061DB32845C11FC7BD87C7C8" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Физика</h4><a href="https://ege.fipi.ru/bank/index.php?proj=BA1F39653304A5B041B656915DC36B38" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Химия</h4><a href="https://ege.fipi.ru/bank/index.php?proj=EA45D8517ABEB35140D0D83E76F14A41" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Русский язык</h4><a href="https://ege.fipi.ru/bank/index.php?proj=AF0ED3F2557F8FFC4C06F80B6803FD26" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>История</h4><a href="https://ege.fipi.ru/bank/index.php?proj=068A227D253BA6C04D0C832387FD0D89" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Обществознание</h4><a href="https://ege.fipi.ru/bank/index.php?proj=756DF168F63F9A6341711C61AA5EC578" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                    </div>
                </div>

                <div class="card">
                    <h3>Основной Государственный Экзамен (РАЗДЕЛ ОГЭ)</h3>
                    <div class="fipi-grid">
                        <div class="fipi-box"><h4>Математика</h4><a href="https://oge.fipi.ru/bank/index.php?proj=DE0E276E497AB3784C3FC4CC20248DC0" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Русский язык</h4><a href="https://oge.fipi.ru/bank/index.php?proj=2F5EE3B12FE2A0EA40B06BF61A015416" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Информатика</h4><a href="https://oge.fipi.ru/bank/index.php?proj=74676951F093A0754D74F2D6E7955F06" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Биология</h4><a href="https://oge.fipi.ru/bank/index.php?proj=0E1FA4229923A5CE4FC368155127ED90" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>География</h4><a href="https://oge.fipi.ru/bank/index.php?proj=0FA4DA9E3AE2BA1547B75F0B08EF6445" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Физика</h4><a href="https://oge.fipi.ru/bank/index.php?proj=B24AFED7DE6AB5BC461219556CCA4F9B" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Химия</h4><a href="https://oge.fipi.ru/bank/index.php?proj=33B3A93C5A6599124B04FB95616C835B" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>История</h4><a href="https://oge.fipi.ru/bank/index.php?proj=3CBBE97571208D9140697A6C2ABE91A0" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                        <div class="fipi-box"><h4>Обществознание</h4><a href="https://oge.fipi.ru/bank/index.php?proj=AE63AB28A2D28E194A286FA5A8EB9A78" target="_blank" class="fipi-link">Открыть тренажер →</a></div>
                    </div>
                </div>
            </div>
        </body></html>
'''
    return render_template_string(html)


@app.route('/delete-news/<int:news_id>', methods=['POST'])
def delete_news(news_id):
    global news_list
    pwd = request.form.get('admin_pwd')
    if pwd == ADMIN_PASSWORD:
        news_list = [n for n in news_list if n['id'] != news_id]
    return redirect('/')


@app.route('/secret-control-panel', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        pwd = request.form.get('password')
        if pwd != ADMIN_PASSWORD:
            return "<h1>Ошибка доступа: неверный пароль.</h1>", 403

        conn = get_db()
        new_photo = request.form.get('schedule_url')
        if new_photo: conn.execute("UPDATE settings SET value=? WHERE key='schedule'", (new_photo,))

        new_main_photo = request.form.get('main_schedule_url')
        if new_main_photo: conn.execute("UPDATE settings SET value=? WHERE key='main_schedule'", (new_main_photo,))

        title = request.form.get('title')
        text = request.form.get('text')
        news_img = request.form.get('news_img')

        if title and text:
            # Намертво записываем новость в дисковую базуschool68.db
            conn.execute("INSERT INTO news (title, text, image) VALUES (?, ?, ?)",
                         (title, text, news_img if news_img else ""))

        conn.commit()
        conn.close()
        return redirect('/')

    html = '''
    <html><head>{{ style|safe }}</head><body>
        <div class="container">
            <div class="header"><h1 style="color: #ff9e64;">Панель управления МБОУ СОШ №68</h1></div>
            <div class="nav-menu"><a href="/" class="nav-link">Вернуться на портал</a></div>

            <form method="POST" class="card">
                <input type="password" name="password" class="form-control" placeholder="Пароль администратора (admin68)..." required>

                <h3>1. Ссылка на фото замен на сегодня</h3>
                <input type="text" name="schedule_url" class="form-control" placeholder="URL-ссылка на бланк замен...">

                <h3>2. Ссылка на фото основного расписания</h3>
                <input type="text" name="main_schedule_url" class="form-control" placeholder="URL-ссылка на основное расписание...">

                <h3>3. Добавить официальную новость школы №68</h3>
                <input type="text" name="title" class="form-control" placeholder="Заголовок пресс-релиза...">
                <input type="text" name="news_img" class="form-control" style="border-color: #73daca;" placeholder="Вставьте сюда URL-ссылку на фотографию к новости (необязательно)...">
                <textarea name="text" class="form-control" style="height: 100px;" placeholder="Текст информационного сообщения..."></textarea>

                <button type="submit" class="btn" style="background: #ff9e64; width:100%;">Применить изменения системы</button>
            </form>

            <div class="card" style="border-color: #f7768e; margin-top: 30px;">
                <h3 style="color: #f7768e;">4. Архив публикаций школы №68 (Быстрое удаление)</h3>
                {% for news in news_list %}
                    <div style="background: #15161e; padding: 12px; margin-bottom: 10px; border-radius: 8px; border: 1px solid #24283b; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #41a5f5;">{{ news.title }}</strong>
                        </div>
                        <form action="/delete-news/{{ news.id }}" method="POST" style="margin:0;">
                            <input type="hidden" name="admin_pwd" value="admin68">
                            <button type="submit" class="btn-danger" style="padding: 6px 12px; margin: 0; font-size: 0.85rem; border:none; color:#fff; cursor:pointer; border-radius:6px;">Удалить</button>
                        </form>
                    </div>
                {% endfor %}
            </div>
        </div>
    </body></html>
    '''
    return render_template_string(html, news_list=news_list, style=STYLE)


if __name__ == '__main__':
    app.run(debug=True)