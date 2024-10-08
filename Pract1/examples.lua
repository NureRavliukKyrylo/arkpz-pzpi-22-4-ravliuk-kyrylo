-- Поганий приклад найменування: змінні без контексту та неправильні імена для булевих функцій
local CHECK = true

function check_Flag(a)
    return a == 1
end

-- Гарний приклад найменування: константи та булеві функції іменуються правильно
local MAX_TRIES = 5

function is_flag_set(value)
    return value == 1
end

-- Поганий приклад найменування класів
local OBJEct12 = {}
local Object = {}
local c = function()

end

-- Гарний приклад найменування класів
local this_is_my_object = {}

local function do_that_thing()

end

-- Поганий приклад найменування класів: Неправильні імена класів
c_myclass = {}  -- Не відповідає CamelCase
data = {}       -- Занадто абстрактне
MyClassMgr = {} -- Використання скорочень

-- Гарний приклад найменування класів: Правильні імена класів
Car = {}
Person = {}
XmlParser = {}

-- Поганий приклад: використання неправильного регістру для класу та методів
CData_Mng = {}
function retrieveData()
    
end

function printInfoData()
    
end

-- Гарний приклад: клас використовує CamelCase, а методи — snake_case
CustomerDataManager = {}

function CustomerDataManager:retrieve_data()
    -- Логіка для отримання даних
    print("Дані успішно отримані!")
end

function CustomerDataManager:print_info_data()
    -- Логіка для виведення інформації
    print("Інформація про дані виведена!")
end

-- Поганий приклад форматування

for i, pkg in ipairs(packages) do
	for name, version in pairs(pkg) do
    if name == searched then
          print(version)
      end
	end
end

-- Гарний приклад форматування

for i, pkg in ipairs(packages) do
    for name, version in pairs(pkg) do
       if name == searched then
          print(version)
       end
    end
 end

-- Поганий приклад структури коду: Відсутність організації, неправильні імена та коментарі

-- Глобальні змінні без контексту
x = 10
y = 20

function a(b)  -- Неправильне ім'я функції
    return x + y + b
end

-- Основна частина коду
for i = 1, 10 do
    if i % 2 == 0 then  -- Неправильне використання однолітерної змінної
        print(a(i))
    end
end

-- Відсутність модулів і структур
function b()  -- Ще одна непослідовна функція
    print("Hello")
end

b()  -- Виклик функції без контексту

-- Гарний  приклад структури коду:

-- Імпорт бібліотеки обробки даних
local DataProcessor = require("data_processor")

-- Оголошення класу
UserManager = {}
UserManager.__index = UserManager

function UserManager:new(user_name)
    local user_instance = setmetatable({}, UserManager)
    user_instance.user_name = user_name
    return user_instance
end

-- Виклик функцій
local user_manager = UserManager:new("JohnDoe")

-- Поганий приклад дотримання принципів рефакторингу: повторюваний код, неясні імена та відсутність коментарів
function calc_area(length, width)
    return length * width
end

function calc_area2(length, width)
    return length * width
end

result1 = calc_area(5, 10)
result2 = calc_area2(7, 3)

-- Гарний приклад дотримання принципів рефакторингу: уникнення дублювання, описові імена, коментарі
function calculate_area(length, width)
    return length * width
end

local rectangle_area = calculate_area(5, 10)
local square_area = calculate_area(7, 7)  -- Використання тієї ж функції для обчислення площі квадрата

-- Поганий приклад оптимізації: глобальні змінні, зайві виклики функцій у циклі
count = 0  -- Глобальна змінна

function calculate_square(n)
    return n * n
end

for i = 1, 100000 do
    count = count + calculate_square(i)  -- Виклик функції в циклі
end
print(count)

-- Гарний приклад оптимізації: використання локальних змінних, обчислення за межами циклу
local count = 0  -- Локальна змінна

local function calculate_square(n)
    return n * n
end

local squares = {}  -- Зберігаємо результати
for i = 1, 100000 do
    squares[i] = calculate_square(i)  -- Заповнення таблиці
end

for _, square in ipairs(squares) do
    count = count + square  -- Підсумок після обчислення
end
print(count)

-- Поганий приклад обробки помилок: відсутня обробка помилок
function divide(a, b)
    return a / b  -- Може викликати помилку при діленні на нуль
end

local result = divide(10, 0)  -- Викликає помилку
print(result)  -- Код аварійно завершується

-- Гарний приклад обробки помилок: використання pcall для обробки помилок
function divide(a, b)
    if b == 0 then
        error("Division by zero error")  -- Генерація власної помилки
    end
    return a / b
end

local status, result = pcall(divide, 10, 0)  -- Захищений виклик функції
if status then
    print(result)
else
    print("Error: " .. result)  -- Обробка помилки
end

-- Поганий приклад документування

function load(r, v)
    -- Код завантаження маніфесту
    -- TODO: реалізувати обробку помилок
end

--Гарний приклад документування

--- Завантажує маніфест з репозиторію.
-- @param repo_url string: URL репозиторію.
-- @param lua_version string: Версія Lua.
-- @return table or (nil, string): Таблиця маніфесту або повідомлення про помилку.
function load_manifest(repo_url, lua_version)
    -- TODO: реалізувати обробку помилок
end

-- Поганий приклад тестування

function add(a, b)
    return a + b
end

-- Тести без використання бібліотеки
print(add(1, 2) == 3)  -- Тестуємо, але без структурованого підходу
print(add(-1, -1) == -2)  -- Інший тест 

--Гарний приклад тестування

local busted = require 'busted'

describe("Функція add", function()
    it("повинна правильно додавати позитивні числа", function()
        assert.are.equal(add(1, 2), 3)
    end)

    it("повинна правильно додавати від'ємні числа", function()
        assert.are.equal(add(-1, -1), -2)
    end)
end)


