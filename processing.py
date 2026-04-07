from spectrum import Spectrum
import rampy as rp
import numpy as np
from scipy import interpolate

def process_lib_spectra(library: list, library_path: str) -> list:
    library_norm = []
    for lib_spec in library:
        try:
            lib_spectrum = Spectrum(f"{library_path}/{lib_spec}")  # Создаем экземпляр класса Spectrum
        except Exception as e:
            print(f"\nОшибка при чтении спектра: {lib_spec}")
            print(f"Причина: {e}\n")
            raise
        lib_corr_y, _ = rp.baseline(lib_spectrum.x, lib_spectrum.y, method="als", niter = 5) #Приводим к базовой линии
        lib_norm_y = rp.normalise(lib_corr_y.flatten(), lib_spectrum.x) #Нормализуем

        full_name = lib_spectrum.path.split("/")[1]
        if "_" in full_name:
            name = full_name.split("_")[0]
        else:
            name = full_name.split(".")[0]

        lib_spectrum.name = name
        lib_spectrum.y = lib_norm_y
        library_norm.append(lib_spectrum)

    return library_norm

def trim(spectrum_x: np.ndarray, spectrum_y: np.ndarray, reference_spectrum_x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    reference_spectrum_x = reference_spectrum_x.astype(float)
    mask = (spectrum_x >= reference_spectrum_x.min()) & (spectrum_x <= reference_spectrum_x.max())
    trimmed_x = spectrum_x[mask]
    trimmed_y = spectrum_y[mask]
    if len(trimmed_x) == 0:
        print("Нет пересечения диапазонов с библиотекой!")
        return np.array([]), np.array([])
    sort_idx = np.argsort(trimmed_x)
    return trimmed_x[sort_idx], trimmed_y[sort_idx]

def interpol(
        spectrum_x: np.ndarray, 
        spectrum_y: np.ndarray, 
        reference_spectrum_x: np.ndarray,
        ) -> np.ndarray:
    
    f = interpolate.interp1d(spectrum_x, spectrum_y, kind="cubic", bounds_error=False, fill_value=0.0)
    interpolated_y = f(reference_spectrum_x)
    return interpolated_y