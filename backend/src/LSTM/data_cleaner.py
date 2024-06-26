import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd


def clean_text(text):
    # Удаление HTML-тегов
    text = re.sub(r'<.*?>', '', text)

    # Удаление лишних пробелов
    text = re.sub(r'\s+', ' ', text)

    # Приведение текста к нижнему регистру
    text = text.lower()

    # Токенизация текста
    tokens = word_tokenize(text)

    # Удаление стоп-слов
    stop_words = set(stopwords.words('russian'))
    filtered_tokens = [token for token in tokens if token not in stop_words]

    # Объединение токенов обратно в текст
    cleaned_text = ' '.join(filtered_tokens)

    return cleaned_text


# Пример использования функции clean_text с отображением прогресса
if __name__ == "__main__":
    # Загрузка данных
    df = pd.read_csv('dataset/train_ru.csv')

    # Применение функции clean_text к столбцу 'comment_text' с отображением прогресса
    total_rows = len(df)
    for i, row in enumerate(df.itertuples(index=False)):
        cleaned_text = clean_text(getattr(row, 'comment_text'))
        df.at[df.index[i], 'cleaned_comment'] = cleaned_text

        # Отображение прогресса
        progress = (i + 1) / total_rows * 100
        print(f"{progress:.2f}%")

    # Сохранение результата в новый файл
    df.to_csv('dataset/train_ru_clear.csv', index=False)
