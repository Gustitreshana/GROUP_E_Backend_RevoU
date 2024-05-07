def format_rupiah(nominal):
    return "Rp{:,.0f}".format(nominal).replace(',', '.')