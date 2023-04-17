def shorten_number_string(num):
    if isinstance(num, str):
        num = float(num)
    m_const = 1000000
    if num >= m_const:
        return f"{num / m_const :.0f}M"
    k_const = 1000
    if num >= k_const:
        return f"{num / k_const :.0f}K"
    else:
        return f"{num:.0f}"
