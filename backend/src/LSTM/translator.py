from deep_translator import GoogleTranslator
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def translate_single(text, output_file):
    try:
        translated_text = GoogleTranslator(source='auto', target='ru').translate(text)
        with open(output_file, 'a', encoding='UTF-8') as file:
            file.write(f"{translated_text}\n")
        return translated_text
    except Exception as e:
        print(f"Failed to translate text: {text}, error: {e}")
        return text


def save_state(file_path, position):
    with open(file_path, 'w') as file:
        file.write(str(position))


def load_state(file_path):
    try:
        with open(file_path, 'r') as file:
            position = int(file.read())
            return position
    except FileNotFoundError:
        return 0


def translate_comments_parallel(df, column_name='comment_text', num_workers=4, state_file='state.txt',
                                output_file='translated_texts.csv'):
    total_rows = len(df)
    translated_rows = current_position = load_state(state_file)

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for i in range(current_position, total_rows):
            future = executor.submit(translate_single, df.loc[i, column_name], output_file)
            futures.append(future)

        for future in futures:
            translated_text = future.result()
            translated_rows += 1
            print(f"{translated_rows}/{total_rows}: {translated_text[:50]}...")
            save_state(state_file, translated_rows)

    return df


# Чтение исходного файла
df = pd.read_csv('dataset/test.csv')

# Параллельный перевод текста в столбце 'comment_text' с использованием GoogleTranslator
translated_df = translate_comments_parallel(df)

# Сохранение результатов в новый файл
translated_df.to_csv('dataset/test_ru.csv', index=False)
