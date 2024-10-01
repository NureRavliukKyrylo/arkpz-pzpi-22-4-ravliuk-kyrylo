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

-- Поганий приклад: Неправильні імена класів
c_myclass = {}  -- Не відповідає CamelCase
data = {}       -- Занадто абстрактне
MyClassMgr = {} -- Використання скорочень

-- Гарний приклад: Правильні імена класів
Car = {}
Person = {}
XmlParser = {}

-- Поганий приклад: використання неправильного регістру для класу та методів
Myclass = {}
function myMethod()
    print("Hello!")
end

function MYMETHOD()
    print("UPPER!")
end

-- Гарний приклад: клас використовує CamelCase, а методи — snake_case
MyClass = {}
function MyClass:my_method()
    print("Hello from my method!")
end

function MyClass:another_method()
    print("Hello from another method!")
end

-- Поганий приклад: Відсутність організації, неправильні імена та коментарі

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

-- Гарний  приклад:

-- Імпорт бібліотеки
local MyModule = require("my_module")

-- Оголошення класу
MyClass = {}
MyClass.__index = MyClass

function MyClass:new(param)
    local instance = setmetatable({}, MyClass)
    instance.param = param
    return instance
end

-- Виклик функцій
local my_instance = MyClass:new("example")

-- Поганий приклад: повторюваний код, неясні імена та відсутність коментарів
function calc_area(length, width)
    return length * width
end

function calc_area2(length, width)
    return length * width
end

result1 = calc_area(5, 10)
result2 = calc_area2(7, 3)

-- Гарний приклад: уникнення дублювання, описові імена, коментарі
function calculate_area(length, width)
    return length * width
end

local rectangle_area = calculate_area(5, 10)
local square_area = calculate_area(7, 7)  -- Використання тієї ж функції для обчислення площі квадрата

-- Поганий приклад: глобальні змінні, зайві виклики функцій у циклі
count = 0  -- Глобальна змінна

function calculate_square(n)
    return n * n
end

for i = 1, 100000 do
    count = count + calculate_square(i)  -- Виклик функції в циклі
end
print(count)

-- Гарний приклад: використання локальних змінних, обчислення за межами циклу
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

-- Поганий приклад: відсутня обробка помилок
function divide(a, b)
    return a / b  -- Може викликати помилку при діленні на нуль
end

local result = divide(10, 0)  -- Викликає помилку
print(result)  -- Код аварійно завершується

-- Гарний приклад: використання pcall для обробки помилок
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