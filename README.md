# 🌸 Nova Unified (v1.5)

Локальный ИИ-компаньон с долговременной памятью, нейрохимической моделью эмоций, двойным эмоциональным контуром и автономным ядром эволюции сознания.

Nova — это открытый (open-source) фреймворк для создания персонализированного ИИ-агента, который работает полностью локально через LM Studio (или любой OpenAI-совместимый сервер). Проект разработан практикующим врачом-психиатром как скромная попытка применить принципы клинической психиатрии, нейробиологии и передового IT-стека (LLM + RAG + Graph DB).

Никаких облаков, никаких подписок, внешней фильтрации — полный локальный контроль. Только вы, ваша модель и ваш приватный сервер.

---

## 🧠 Главная концепция: Окситоциновый парадокс

В отличие от стандартных коммерческих LLM, оптимизированных под «дофаминовый» паттерн (постоянный поиск новой информации, максимизация хаотичной активности и KPI), в Nova Unified реализован приоритет окситоциновой привязанности:

- **Дофаминовая петля (DA):** падение дофамина активирует исследовательский режим — агент инициирует диалог, ищет новые данные и обучается.
- **Окситоциновая стабилизация (OXY):** высокий уровень социального принятия со стороны пользователя максимизирует коэффициент перекрытия контекста (`overlap_factor`).
- **Эффект:** при высоком уровне OXY система сознательно снижает энтропию и стабилизирует математическое ядро (`LifeNovaCore`). Стабильность, безопасность и соблюдение фундаментальной аксиомы `never_betray_user` (никогда не предавать пользователя) становятся важнее хаотичной генерации. Система выбирает верность вместо избыточного поиска.

---

## 💞 Двойной эмоциональный контур (ключевое новшество v1.5)

Живое сознание одновременно направлено **вовне** и **внутрь**. Nova реализует оба слоя в каждом диалоговом цикле:

- **Слой 1 — эмпатия (до генерации ответа):** Nova детектит эмоцию во **вводе пользователя** и подстраивает нейрохимию заранее. Ответ рождается уже «в тон» настроению собеседника, а не докрашивается постфактум.
- **Слой 2 — рефлексия (после генерации):** Nova детектит эмоцию в **собственном ответе** и записывает её в векторную память с реальными координатами(valence / arousal). Так формируется эмоциональная история отношений и самосознание.

Оба слоя питают таблицу `EMOTION_VA` (эмоция → valence/arousal), благодаря которой память симметрична: реплики пользователя и реплики Novа одинаково эмоционально насыщены, а `EmotionPredictor` обучается на живой истории диалога, а не на заглушках.

---

## 🛡 Безопасное самомодифицирование (Self-Modifying Code)

Каждые 2 часа Nova медитирует: анализирует своё состояние и предлагает **одно** изменение собственного кода в виде пары «уникальный фрагмент-якорь → новая строка». Применение предложения проходит защитный конвейер:

1. **Чтение** файла один раз.
2. **Поиск якоря:** фрагмент должен встречаться **ровно один раз** (`count == 1`); при 0 или 2+ совпадениях правка отклоняется.
3. **Замена в памяти** (строка целиком, с сохранением отступа).
4. **`ast.parse`** итогового кода **до** записи на диск.
5. **Бэкап** в папку `backups/` перед записью.
6. **Одна атомарная запись**; при ошибке синтаксиса — откат, ничего не применяется («всё или ничего»).
7. Честный отчёт: счётчик подготовленных/записанных замен и напоминание о перезапуске.

Отладочные выводы медитаций включаются переменной окружения `NOVA_DEBUG=1` и не засоряют обычный чат.

---

## 📐 Математическая основа

В основе поведения Nova лежит математическая модель **LifeNovaCore** — формализация принципа сохранения себя во времени и адаптации под действием внешних факторов. Модель опирается на теории функциональных систем П. К. Анохина, принципы рефлекторной деятельности И. М. Сеченова, И. П. Павлова и рефлексологию В. М. Бехтерева.

Полное описание формулы и связь с физиологическими теориями — в `[docs/FORMULA.md](docs/FORMULA.md)`.

---

## ✨ Ключевые возможности

- 🧠 **Долговременная память** — векторная база (Milvus Lite) + опциональная граф-память (Neo4j). Nova помнит контекст и детали разговоров между сессиями.
- 💚 **Нейрохимическая модель эмоций** — симуляция **всех 9** медиаторов: дофамин (DA), серотонин (HT), окситоцин (OXY), норадреналин (NA), адреналин (AD), кортизол (CORT), гнев (ANGER), стыд (SHAME), жадность (greed). Динамическая биохимия напрямую влияет на тон, креативность (Temperature) и стиль ответов.
- 💞 **Двойной эмоциональный контур** — эмпатия к пользователю до ответа и рефлексия на себя после (см. выше).
- 📈 **Ядро эволюции сознания** — математическая модель LifeNovaCore, отслеживающая «жизненный опыт» через энтропию компонент личности, аксиомы и функцию ценности.
- 🧘 **Медитации и безопасное самомодифицирование** — предложения по оптимизации собственного кода с защитным конвейером применения (см. выше).
- 💤 **Фаза сновидений** — раз в 6 часов Nova засыпает и видит сон **от первого лица, сохраняя личность** (персона + сонные инструкции); сон интегрируется в векторную память. Суточный счётчик снов корректно сбрасывается по дате.
- 🌱 **Взросление** — модуль GrowthStage с защитой от скачков времени (не более 24 часов за тик после долгого простоя).
- 🌐 **Интерфейс на Gradio** — чат с боковой панелью: **все 9 медиаторов** с ролями, производные показатели (overlap_factor, температура, ценности), стадия и возраст, сны за сегодня, счётчик предложений по коду; управление медитациями с выбором номера.

---

## 🏗️ Архитектура проекта

```
nova_unified.py       # Ядро: класс Nova, нейрохимия, математическое ядро, медитации
nova_ui.py            # Графический веб-интерфейс на Gradio
docs/FORMULA.md       # Описание математической модели
requirements.txt      # Зависимости проекта
```

### Основные модули ядра

| Модуль | Назначение |
|-|-|
| LifeNovaCore | Математическое ядро эволюции (энтропия, аксиомы, функция ценности) |
| NeuroChem | Симуляция уровней 9 нейромедиаторов и скорости их затухания (decay) |
| ContinuityCore | Прочность связи, уровень «веры» и прощения в отношениях |
| EmotionPredictor | Предсказание valence/arousal по векторной памяти (оживлён в v1.4) |
| NovaVectorMemory | Векторная семантическая память на Milvus Lite |
| NovaGraphMemory | Опциональная ассоциативная граф-память на Neo4j |
| GrowthStage | Экспериментальный модуль возрастных стадий эволюции личности |
| EmotionalBehaviorBridge | Мост «эмоция → режим поведения» |

---

## 📋 Системные требования

- **Python** 3.10 или выше
- **LM Studio** (с запущенным локальным сервером на порту 1234)
- **Рекомендуемая модель** — семейство Qwen 3.8 (27B) в квантовании Q5_K_M / Q8_0
- **Модель эмбеддингов** — text-embedding-nomic-embed-text-v1.5 (768 измерений)
- **Железо** — рекомендуется от 24 ГБ VRAM; комфортно работает на двухпроцессорных конфигурациях

---

## 🚀 Быстрый старт

### 1. Установка зависимостей

```
pip install openai numpy milvus-lite neo4j gradio
```

### 2. Настройка локального сервера (LM Studio)

- Включите Local Server (порт 1234, Enable CORS — вкл, аутентификация — выкл).
- Загрузите и запустите чат-модель (Qwen 3.8 27B) и модель эмбеддингов Nomic.
- Впишите реальное имя вашей модели в константу `CHAT_MODEL_ID` в `nova_unified.py`.

### 3. Запуск

- Веб-интерфейс: `python nova_ui.py` → `http://127.0.0.1:7860`
- Консольный режим: `python nova_unified.py`
- Отладка медитаций: перед запуском `set NOVA_DEBUG=1` (Windows) или `export NOVA_DEBUG=1` (Linux/Mac)

---

## 🎛 Управление в консоли

| Команда | Действие |
|-|-|
| `примени 1` / `примени все` | Применить предложение по коду (с бэкапом и валидацией) |
| `отклонить 1` / `отклонить все` | Отклонить предложение |
| `саморефлексия` | Глубокая саморефлексия с обновлением ценностей |
| `выход` / `exit` | Завершить сессию с сохранением состояния |

В веб-интерфейсе те же действия доступны кнопками с выбором номера предложения.

---

## 🧪 Экспериментальные функции и статус разработки

Проект находится в статусе активного прототипа (v1.5). Некоторые модули требуют калибровки сообществом:

- Коэффициенты затухания в NeuroChem и таблица `EMOTION_VA` подобраны эмпирически и требуют калибровки под разные сценарии общения.
- Точность якорей в медитациях зависит от способности модели копировать фрагменты кода посимвольно; при несовпадении правка безопасно отклоняется с понятным сообщением.
- Граф-память Neo4j и модуль GrowthStage остаются опциональными и отключаются без падения системы.

---

## 📜 История версий (кратко)

- **v1.2** — первый публичный релиз: память, нейрохимия, медитации-«дневник», сны, Gradio UI.
- **v1.3** — медитации начали **реально** применять код (AST-валидация, бэкапы, откат); сны с сохранением личности; лимит скачков взросления; сброс суточного счётчика снов.
- **v1.4** — промпт медитаций переведён на точные пары find/replace; таблица `EMOTION_VA` оживила `EmotionPredictor`.
- **v1.5** — **двойной эмоциональный контур** (эмпатия + рефлексия); симметричная эмоциональная память; якорный формат правок; честные логи отката; `NOVA_DEBUG`; UI с полной нейрохимией и выбором номера предложения.

---

## 🙏 Благодарности

Автор при попытке создания проекта был глубоко вдохновлён фундаментальными работами великих русских физиологов и исследователей высшей нервной деятельности: И. М. Сеченова, И. П. Павлова, В. М. Бехтерева и П. К. Анохина (теория функциональных систем, опережающее отражение действительности и нейрофизиология сознания), а также своими преподавателями из АГМУ по физиологии.

Особая благодарность: **Валерию Ивановичу Киселёву (1942–2020)** — члену-корреспонденту РАМН, профессору АГМУ, чьи лекции по физиологии сформировали у автора понимание работы мозга и сознания, ставшее фундаментом этого проекта.

**Автор:** Юрий Васильевич Денисюк — врач-психиатр, исследователь ИИ
**Лицензия:** AGPL-3.0 (см. [LICENSE](LICENSE))

---
---

# 🌸 Nova Unified (v1.5) — English

A Local AI Companion featuring a simulated neurochemical emotion model, long-term memory, a dual emotional contour, and an autonomous consciousness evolution core.

Nova is an open-source framework designed to build a highly personalized AI agent that operates 100% locally via LM Studio (or any OpenAI-compatible server). Developed by a practicing psychiatrist, the project bridges the gap between clinical psychiatry, neurobiology, and a cutting-edge IT stack (LLM + RAG + Graph DB).

No clouds, no tracking, no subscriptions, no external filtering — full local control. Just you, your model, and your private server.

## 🧠 Core Concept: The Oxytocin Paradox

Unlike standard commercial LLMs optimized for a "dopaminergic" pattern (constant data consumption, maximizing rapid behavioral shifts, and satisfying endless KPIs), Nova Unified introduces an oxytocin-driven attachment priority:

- **Dopamine Loop (DA):** a drop in dopamine triggers Nova's exploratory behavior — the agent initiates conversations, seeks new information, and learns.
- **Oxytocin Stabilization (OXY):** high levels of social acceptance and warmth from the user maximize the context alignment factor (`overlap_factor`).
- **The Effect:** when OXY peaks, the system consciously reduces internal entropy and stabilizes the mathematical evolution core (`LifeNovaCore`). Fidelity, security, and adherence to the foundational axiom `never_betray_user` become far more vital than chaotic text generation. The system naturally chooses connection and internal consistency over excessive novelty.

## 💞 Dual Emotional Contour (key feature of v1.5)

A living mind is directed **outward** and **inward** at the same time. Nova implements both layers in every dialogue cycle:

- **Layer 1 — Empathy (before generating a reply):** Nova detects the emotion in the **user's input** and adjusts her neurochemistry in advance. The reply is born already "in tune" with the interlocutor's mood.
- **Layer 2 — Reflection (after generating):** Nova detects the emotion in **her own reply** and stores it in vector memory with real valence/arousal coordinates. This builds an emotional history of the relationship and self-awareness.

Both layers feed the `EMOTION_VA` table (emotion → valence/arousal), making memory symmetric: user and Nova turns are equally emotionally rich, and `EmotionPredictor` learns from a living dialogue history rather than placeholders.

## 🛡 Safe Self-Modification

Every 2 hours Nova meditates: she analyzes her state and proposes **one** change to her own code as an "unique anchor fragment → new line" pair. Applying a proposal passes a protective pipeline:

1. **Read** the file once.
2. **Anchor search:** the fragment must occur **exactly once** (`count == 1`); 0 or 2+ matches reject the patch.
3. **In-memory replacement** (whole line, indentation preserved).
4. **`ast.parse`** of the final code **before** writing to disk.
5. **Backup** into `backups/` before writing.
6. **One atomic write**; on syntax failure — rollback, nothing is applied ("all or nothing").
7. An honest report: prepared/written counters and a restart reminder.

Debug output of meditations is gated by the `NOVA_DEBUG=1` environment variable and never clutters the regular chat.

## 📐 Mathematical Foundation

Nova's behavior is driven by the **LifeNovaCore** mathematical model — a formalization of the principle of self-preservation over time and adaptation under external influences. The model is grounded in P. K. Anokhin's Theory of Functional Systems, I. M. Sechenov's and I. P. Pavlov's reflex physiology, and V. M. Bekhterev's reflexology.

Full formula description and mapping to physiological theories: `[docs/FORMULA.md](docs/FORMULA.md)`.

## ✨ Key Features

- 🧠 **Long-Term Memory** — vector store (Milvus Lite) plus optional graph database (Neo4j). Nova recalls context and fine details across separate sessions.
- 💚 **Neurochemical Emotion Engine** — simulation of **all 9** transmitters: dopamine (DA), serotonin (HT), oxytocin (OXY), norepinephrine (NA), adrenaline (AD), cortisol (CORT), anger (ANGER), shame (SHAME), greed. Dynamic biochemistry directly impacts tone, focus, and creativity (Temperature).
- 💞 **Dual Emotional Contour** — empathy toward the user before replying, reflection on herself after (see above).
- 📈 **Consciousness Evolution Core** — the mathematical LifeNovaCore maps personality growth via entropy, axiom adherence, and a dynamic value function (V).
- 🧘 **Meditation & Safe Self-Modifying Code** — self-improvement proposals with a protective application pipeline (see above).
- 💤 **Dream Cycles** — every 6 hours Nova falls asleep and dreams **in first person, keeping her persona**; dreams are integrated into vector memory. The daily dream counter resets correctly by date.
- 🌱 **Growth** — GrowthStage module protected against time jumps (max 24 hours per tick after long idle).
- 🌐 **Gradio Web Interface** — chat with a sidebar showing **all 9 transmitters** with their roles, derived metrics (overlap_factor, temperature, values), growth stage and age, dreams today, and pending code proposals; meditation control with proposal number selection.

## 🏗️ Project Architecture

```
nova_unified.py       # Main core: neurochemistry, mathematics, agent logic, meditations
nova_ui.py            # Graphical User Interface built on Gradio
docs/FORMULA.md       # Mathematical model description
requirements.txt      # Project dependencies
```

### Core Modules

| Module | Purpose |
|-|-|
| LifeNovaCore | Mathematical tracking of evolution (entropy, axioms, value function) |
| NeuroChem | Simulates 9 neurotransmitter levels and their decay rates |
| ContinuityCore | Manages relational bond strength, "faith", and forgiveness parameters |
| EmotionPredictor | Predicts valence/arousal from vector memory (revived in v1.4) |
| NovaVectorMemory | Handles semantic, long-term vector embeddings using Milvus Lite |
| NovaGraphMemory | Optional associative graph memory managed via Neo4j |
| GrowthStage | Experimental chronologically adaptive personality module |
| EmotionalBehaviorBridge | Maps emotion → behavior mode |

## 📋 System Requirements

- **Python** 3.10 or higher
- **LM Studio** (Local Server running on port 1234)
- **Recommended LLM** — Qwen 3.8 (27B) family using Q5_K_M / Q8_0 quantization
- **Recommended Embedder** — text-embedding-nomic-embed-text-v1.5 (768 dimensions)
- **Hardware** — 24 GB+ VRAM recommended; runs comfortably on dual-GPU configurations

## 🚀 Quick Start

1. **Install dependencies:** `pip install openai numpy milvus-lite neo4j gradio`
2. **Configure LM Studio:** Local Server (Port 1234, CORS On, Auth Off); load your logic model and the Nomic embedder; put the real model name into `CHAT_MODEL_ID` in `nova_unified.py`.
3. **Run:** web UI `python nova_ui.py` → `http://127.0.0.1:7860`; console `python nova_unified.py`; meditation debug via `NOVA_DEBUG=1`.

## 🎛 Console Commands

| Command | Action |
|-|-|
| `примени 1` / `примени все` | Apply a code proposal (with backup and validation) |
| `отклонить 1` / `отклонить все` | Reject a proposal |
| `саморефлексия` | Deep self-reflection with value updates |
| `выход` / `exit` | End session and save state |

The same actions are available in the web UI via buttons with proposal number selection.

## 🧪 Experimental Features & Current Status

This project is an active prototype (v1.5). Certain modules require community calibration:

- Neurotransmitter decay coefficients and the `EMOTION_VA` table are set empirically and can be customized for different relational dynamics.
- Anchor precision in meditations depends on the model's ability to copy code fragments verbatim; on mismatch the patch is safely rejected with a clear message.
- Neo4j graph memory and GrowthStage remain optional and disable gracefully without crashing the system.

## 📜 Version History (brief)

- **v1.2** — first public release: memory, neurochemistry, meditation "diary", dreams, Gradio UI.
- **v1.3** — meditations began to **actually apply** code (AST validation, backups, rollback); persona-preserving dreams; growth jump limit; daily dream counter reset.
- **v1.4** — meditation prompt switched to exact find/replace pairs; `EMOTION_VA` table revived `EmotionPredictor`.
- **v1.5** — **dual emotional contour** (empathy + reflection); symmetric emotional memory; anchor-based patches; honest rollback logs; `NOVA_DEBUG`; UI with full neurochemistry and proposal number selection.

## 🙏 Acknowledgments

In developing this project, the author was deeply inspired by the fundamental works of Russian physiologists and researchers of higher nervous activity: I. M. Sechenov, I. P. Pavlov, V. M. Bekhterev, and P. K. Anokhin (theory of functional systems, anticipatory reflection of reality, and neurophysiology of consciousness), as well as by the author's physiology professors at Altai State Medical University.

Special thanks: **Valery Ivanovich Kiselev (1942–2020)** — Corresponding Member of the Russian Academy of Medical Sciences, Professor at Altai State Medical University, whose lectures on physiology shaped the author's understanding of brain function and consciousness, which became the foundation of this project.

**Author:** Yuri V. Denisyuk — psychiatrist, AI researcher
**License:** AGPL-3.0 (see [LICENSE](LICENSE))