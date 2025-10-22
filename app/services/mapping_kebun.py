import logging

logger = logging.getLogger("APN-Riau.kebun_mapping")

# === Mapping NamaKebun → KodeKebun ===
KEBUN_CODE_MAP = {
    "KENCANA AMAL TANI 1": "KAT1",
    "KENCANA AMAL TANI 2": "KAT2",
    "KENCANA AMAL TANI 3": "KAT3",
    "BANYU BENING UTAMA 1": "BBU1",
    "BANYU BENING UTAMA 2": "BBU2",
    "PANCA AGRO LESTARI": "PAL",
    "PALMA S-1": "PS1",
    "PALMA S-2": "PS2",
}

def get_kode_kebun(nama_kebun: str) -> str | None:
    """
    Mengembalikan kode kebun berdasarkan nama kebun.
    Jika nama tidak ditemukan, akan log peringatan dan return None.
    """
    if not nama_kebun:
        return None

    kode = KEBUN_CODE_MAP.get(nama_kebun)
    if not kode:
        logger.warning(f"Nama kebun tidak dikenali: {nama_kebun}")
    return kode