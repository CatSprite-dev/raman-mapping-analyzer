import os
import numpy as np
import rampy as rp
import pandas as pd
from max_heap import MaxHeap
from tqdm import tqdm
from dotenv import load_dotenv
from file_io import detect_separator, validate_dataframe_of_map
from processing import process_lib_spectra, trim, interpol
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning) # Подавляем предупреждение rampy о делении на ноль при нормализации

def main():
    load_dotenv()
    map_path = os.environ.get("MAP_PATH")
    sep = detect_separator(map_path)
    df = validate_dataframe_of_map(pd.read_csv(map_path, sep=sep)) #создаем DataFrame pandas и валидируем его
    grouped = df.groupby(['X', 'Y']) #Группируем строки по уникальным значениям X и Y
    
    print(f"\033[32m\n===| {map_path} |===\n\033[0m")
    
    spectra = []
    coordinates = []
    width = len("Приведение к базовой линии")
    for coord, group in tqdm(grouped, desc=f"{'Получение спектров':{width}}", ncols=120, bar_format='{l_bar}{bar:40}|{n_fmt}/{total_fmt}'):
        spectrum = group[['W', 'I']].values #Создаём np массив вида [[W1, I1], [W2, I2], ...]
        spectrum_sorted = spectrum[spectrum[:, 0].argsort()] #Сортируем массив
        spectra.append(spectrum_sorted)
        coordinates.append(coord)
        
    corrected_spectra = []
    baselines = []
    for spectrum in tqdm(spectra, desc=f"{'Приведение к базовой линии':{width}}", ncols=120, colour="blue", bar_format='{l_bar}{bar:40}|{n_fmt}/{total_fmt}'):
        x = spectrum[:, 0] #Первый столбик W
        y = spectrum[:, 1] #Второй столбик I
        correct_y, baseline = rp.baseline(x, y, method="als", niter = 5) #Приводим спектр к базовой линии 
        corrected_spectra.append(np.column_stack((x, correct_y))) #Создаем двумерный массив np из одномерных массивов x и y(correcr_y)
        baselines.append(np.column_stack((x, baseline))) #То же самое и для базовой линии
    
    normalised_spectra = []
    for spectrum in corrected_spectra: 
        x = spectrum[:, 0] #Первый столбик W
        y = spectrum[:, 1] #Второй столбик I
        normalise_y = rp.normalise(y, x) #Нормализуем спектры, чтобы интенсивность была в пределах от 0 до 1
        normalised_spectra.append(np.column_stack((x, normalise_y))) #Создаем двумерный np массив из одномерных массивов x и normalise_y
    
    library_path = os.environ.get("LIBRARY_PATH")
    library = os.listdir(library_path) #Получаем список спектров в папке
    library_norm = process_lib_spectra(library, library_path)

    common_count = 0
    result = {} 
    for spec in tqdm(normalised_spectra, desc=f"{'Подсчет результатов':{width}}", ncols=120, colour="red", bar_format='{l_bar}{bar:40}|{n_fmt}/{total_fmt}'):
        heap = MaxHeap()
        for lib_norm in library_norm:
            trimmed_x, trimmed_y = trim(spec[:, 0], spec[:, 1], lib_norm.x) #Обрезаем спеткр до диапазона библиотечного
            interpolated_y = interpol(trimmed_x, trimmed_y, lib_norm.x) #Интерполируем обрезанный спектр на библиотечный
            corr_coef = np.around(np.corrcoef(interpolated_y, lib_norm.y)[0,1], 2) #Высчитываем коэфициент корреляции

            if corr_coef > 0.50:
                heap.push(corr_coef, lib_norm.name)

        common_count += 1
        value = heap.peek()
        if value is not None:
            if value not in result:
                result[value] = 0
            result[value] += 1
     
    print(f"Общее количество спектров = {common_count}")
    
    for key, value in sorted(result.items()):
        print(f"{key} - {value}" )
        
if __name__ == "__main__":
    main()
