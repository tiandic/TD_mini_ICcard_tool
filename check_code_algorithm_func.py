import hashlib

def cumulative_sum(data_bytes: bytes, mask=0xFF) -> int:
    """
    计算累加和，并应用掩码。

    参数:
    data_bytes (bytes): 输入的字节序列。
    mask (int): 掩码，用于限定结果的位宽。

    返回:
    int: 计算得到的累加和。
    """
    result = sum(data_bytes)
    return result & mask

def calculate_xor_checksum(data_bytes: bytes, mask=0xFF) -> int:
    """
    计算异或校验和，并应用掩码。

    参数:
    data_bytes (bytes): 输入的字节序列。
    mask (int): 掩码，用于限定结果的位宽。

    返回:
    int: 计算得到的异或校验和。
    """
    checksum = 0
    for byte in data_bytes:
        checksum ^= byte
    return checksum & mask

def crc16_ccitt(data_bytes: bytes, poly=0x1021, mask=0xFF) -> int:
    """
    计算 CRC-16-CCITT 校验码，并应用掩码。

    参数:
    data_bytes (bytes): 输入的字节序列。
    poly (int): 生成多项式，默认值为 0x1021。
    mask (int): 掩码，用于限定结果的位宽。

    返回:
    int: 计算得到的 CRC-16-CCITT 校验码。
    """
    crc = 0xFFFF
    for byte in data_bytes:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc & mask

def calculate_lrc(data_bytes: bytes, mask=0xFF) -> int:
    """
    计算纵向冗余校验（LRC）码，并应用掩码。

    参数:
    data_bytes (bytes): 输入的字节序列。
    mask (int): 掩码，用于限定结果的位宽。

    返回:
    int: 计算得到的 LRC 校验码。
    """
    lrc = sum(data_bytes) & 0xFF
    lrc = ((lrc ^ 0xFF) + 1) & 0xFF
    return lrc & mask

def fletcher16(data_bytes: bytes, mask=0xFF) -> int:
    """
    计算 Fletcher-16 校验和，并应用掩码。

    参数:
    data_bytes (bytes): 输入的字节序列。
    mask (int): 掩码，用于限定结果的位宽。

    返回:
    int: 计算得到的 Fletcher-16 校验和。
    """
    sum1 = 0
    sum2 = 0
    for byte in data_bytes:
        sum1 = (sum1 + byte) % 255
        sum2 = (sum2 + sum1) % 255
    return ((sum2 << 8) | sum1) & mask

def adler32(data_bytes: bytes, mask=0xFF) -> int:
    """
    计算 Adler-32 校验和，并应用掩码。

    参数:
    data_bytes (bytes): 输入的字节序列。
    mask (int): 掩码，用于限定结果的位宽。

    返回:
    int: 计算得到的 Adler-32 校验和。
    """
    MOD_ADLER = 65521
    a = 1
    b = 0
    for byte in data_bytes:
        a = (a + byte) % MOD_ADLER
        b = (b + a) % MOD_ADLER
    return ((b << 16) | a) & mask

def crc32(data_bytes: bytes, mask=0xFF) -> int:
    """
    计算 CRC-32 校验码，并应用掩码。

    参数:
    data_bytes (bytes): 输入的字节序列。
    mask (int): 掩码，用于限定结果的位宽。

    返回:
    int: 计算得到的 CRC-32 校验码。
    """
    import binascii
    return binascii.crc32(data_bytes) & mask

def crc8(data_bytes: bytes, polynomial: int = 0x07, initial_value: int = 0x00, mask: int = 0xFF) -> int:
    """
    计算 CRC-8 校验码。

    参数:
    data_bytes (bytes): 输入的字节序列。
    polynomial (int): 生成多项式，默认值为 0x07。
    initial_value (int): 初始值，默认值为 0x00。
    mask (int): 掩码，用于限定结果的位宽，默认值为 0xFF。

    返回:
    int: 计算得到的 CRC-8 校验码。
    """
    crc = initial_value
    for byte in data_bytes:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ polynomial) & mask
            else:
                crc = (crc << 1) & mask
    return crc

def crc16_iso14443(data_bytes: bytes, polynomial: int = 0x8408, initial_value: int = 0xFFFF, mask: int = 0xFF) -> int:
    """
    计算 ISO/IEC 14443 标准的 CRC-16 校验码。

    参数:
    data_bytes (bytes): 输入的字节序列。
    polynomial (int): 生成多项式，默认值为 0x8408。
    initial_value (int): 初始值，默认值为 0xFFFF。
    mask (int): 掩码，用于限定结果的位宽，默认值为 0xFFFF。

    返回:
    int: 计算得到的 CRC-16 校验码。
    """
    crc = initial_value
    for byte in data_bytes:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = ((crc >> 1) ^ polynomial) & mask
            else:
                crc = (crc >> 1) & mask
    return crc

def crc16_xmodem(data_bytes: bytes, mask: int = 0xFF) -> int:
    """
    计算 CRC-16 XMODEM 校验码。

    参数:
    data_bytes (bytes): 输入的字节序列。
    mask (int): 掩码，用于限定结果的位宽，默认值为 0xFFFF。

    返回:
    int: 计算得到的 CRC-16 XMODEM 校验码。
    """
    poly = 0x1021  # CRC-16 XMODEM 多项式
    crc = 0x0000
    for byte in data_bytes:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ poly) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc & mask

def mod11_check(data_bytes: bytes, mask=0xFF) -> int:
    coefficients = [2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7]  # 示例系数
    total_sum = sum(byte * coef for byte, coef in zip(data_bytes, coefficients))
    remainder = total_sum % 11
    return remainder & mask

def md5_checksum(data_bytes: bytes, mask=0xFF) -> int:
    md5_hash = hashlib.md5()
    md5_hash.update(data_bytes)
    digest = md5_hash.digest()
    return int.from_bytes(digest[:4], byteorder='big') & mask

def calculate_sha1(data_bytes: bytes, mask=0xFF) -> int:
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data_bytes)
    digest = sha1_hash.digest()
    return int.from_bytes(digest[:4], byteorder='big') & mask

def calculate_sha256(data_bytes: bytes, mask=0xFF) -> int:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data_bytes)
    digest = sha256_hash.digest()
    return int.from_bytes(digest[:4], byteorder='big') & mask

