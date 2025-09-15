import requests
import streamlit as st

st.title("Кредитная карта Premium")
st.write("Новая кредитная карта с мгновенным одобрением")

with st.form("Подать заявку"):
    age = st.number_input("Ваш возраст", min_value=18)
    income = st.number_input("Ваш доход в миллион сумах", min_value=0)
    education = st.checkbox("У меня есть высшее образование")
    work = st.checkbox("У меня есть стабильная работа")
    car = st.checkbox("У меня есть автомобиль")
    submit = st.form_submit_button("Подать заявку")

if submit:
    data = {"age": age, "income": income, "education": education, "work": work, "car": car}

    try:
        response = requests.post("http://127.0.0.1:8000/score", json=data, timeout=10)
        response.raise_for_status()

        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError:
            st.error(f"Сервер вернул неверный ответ. Статус: {response.status_code}, Содержимое: {response.text[:200]}")
        else:
            if result.get("approved"):
                st.success("Поздравляем, ваша заявка одобрена!")
            else:
                st.warning("Подобрали для вас альтернативу - дебетовая карта с 3% кешбеком.")

    except requests.exceptions.ConnectionError:
        st.error("Не удается подключиться к серверу. Убедитесь, что API сервер запущен на http://127.0.0.1:8000")
    except requests.exceptions.Timeout:
        st.error("Превышено время ожидания ответа от сервера")
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при отправке запроса: {e}")
    except Exception as e:
        st.error(f"Неожиданная ошибка: {e}")