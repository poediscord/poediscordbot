def shorten_number_string(num, decimals=0):
    if not isinstance(decimals, int):
        decimals = 0
    if isinstance(num, str):
        num = float(num)
    m_const = 1000000
    if num >= m_const:
        return f"{num / m_const :.{decimals}f}M"
    k_const = 1000
    if num >= k_const:
        return f"{num / k_const :.{decimals}f}K"
    else:
        return f"{num:.0f}"
