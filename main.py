import pandas as pd
import streamlit as st
import locale
import plotly.express as px
locale.setlocale(locale.LC_NUMERIC, 'id_ID')

# Membaca file Excel


@st.cache_data
def load_data():
    df = pd.read_excel('data/ebugeting-perubahan-2023.xlsx')
    return df


# Membuat salinan dari DataFrame
df_copy = load_data()

st.markdown('<link rel="stylesheet" href="/style/style.css" />',
            unsafe_allow_html=True)
sidebar = st.sidebar
sidebar.title('Navigation')
selectopd = sidebar.selectbox(
    'SKPD',
    ['Semua SKPD'] + df_copy['SKPD'].unique().tolist()
)


if selectopd != 'Semua SKPD':
    skpd = df_copy[df_copy['SKPD'] == selectopd]
    st.html(f'<h3>{selectopd}</h3>')
    total_pagu_sebelum = locale.format_string(
        "%d", skpd['JUMLAH'].sum(), grouping=True)
    total_pagu_sesudah = locale.format_string(
        "%d", skpd['JUMLAH PERUBAHAN'].sum(), grouping=True)
    selisih_pagu = locale.format_string(
        "%d", skpd['JUMLAH PERUBAHAN'].sum() - skpd['JUMLAH'].sum(), grouping=True)

    st.markdown(
        f'''
            <table class="table table-bordered">
                <tr>
                    <th>Pagu Sebelum</th>
                    <td>{total_pagu_sebelum}</td>
                </tr>
                <tr>
                    <th>Pagu Sesudah</th>
                    <td>{total_pagu_sesudah}</td>
                </tr>
                <tr>
                    <th>Selisih</th>
                    <td>{selisih_pagu}</td>
                </tr>
            </table>
            <br />
        ''', unsafe_allow_html=True)
    subkegiatan = st.selectbox(
        'Sub Kegiatan', ['Semua Subkegiatan'] + skpd['SUBKEGIATAN'].unique().tolist())
    if subkegiatan != 'Semua Subkegiatan':
        skpd = skpd[skpd['SUBKEGIATAN'] == subkegiatan]
        unique_program = ', '.join(skpd['PROGRAM'].unique())
        unique_kegiatan = ', '.join(skpd['KEGIATAN'].unique())
        unique_subkegiatan = ', '.join(skpd['SUBKEGIATAN'].unique())
        pagu_subkeg_sebelum = locale.format_string(
            "%d", skpd['JUMLAH'].sum(), grouping=True)
        pagu_subkeg_sesudah = locale.format_string(
            "%d", skpd['JUMLAH PERUBAHAN'].sum(), grouping=True)
        pagu_subkeg_selisih = locale.format_string(
            "%d", skpd['JUMLAH PERUBAHAN'].sum() - skpd['JUMLAH'].sum(), grouping=True)
        cek_subkeg_selisih = skpd['JUMLAH PERUBAHAN'].sum(
        ) - skpd['JUMLAH'].sum()
        pagu_subkeg_status = ''
        if cek_subkeg_selisih < 0:
            pagu_subkeg_status += 'BERKURANG'
        elif cek_subkeg_selisih > 0:
            pagu_subkeg_status += 'BERTAMBAH'
        else:
            pagu_subkeg_status += 'TETAP'

        st.markdown(f'''
                <table>
                    <tbody>
                        <tr>
                            <th style="text-wrap: nowrap;">Program</th>
                            <td>{unique_program}</td>
                        </tr>
                        <tr>
                            <th style="text-wrap: nowrap;">Kegiatan</th>
                            <td>{unique_kegiatan}</td>
                        </tr>
                        <tr>
                            <th style="text-wrap: nowrap;">Sub Kegiatan</th>
                            <td>{unique_subkegiatan}</td>
                        </tr>
                        <tr>
                            <th style="text-wrap: nowrap;">Pagu Sebelum</th>
                            <td>{pagu_subkeg_sebelum}</td>
                        </tr>
                        <tr>
                            <th style="text-wrap: nowrap;">Pagu Sesudah</th>
                            <td>{pagu_subkeg_sesudah}</td>
                        </tr>
                        <tr>
                            <th style="text-wrap: nowrap;">Pagu Selisih</th>
                            <td>
                                {pagu_subkeg_selisih} - <small>{pagu_subkeg_status}</small>
                            </td>
                        </tr>
                    </tbody>
                </table>
            <br />
        ''', unsafe_allow_html=True)

        unique_subkeluaran = skpd[
            'SUBKELUARAN'].unique()

        for row in unique_subkeluaran:
            filterDana = skpd[skpd['SUBKELUARAN'] == row]
            sumberdana = ','.join(filterDana['SUMBERDANA'].unique())
            jumlahDanaSebelum = locale.format_string(
                "%d", filterDana['JUMLAH'].sum(), grouping=True)
            jumlahDanaSesudah = locale.format_string(
                "%d", filterDana['JUMLAH PERUBAHAN'].sum(), grouping=True)
            jumlahDanaSelisih = filterDana['JUMLAH PERUBAHAN'].sum(
            ) - filterDana['JUMLAH'].sum()
            st.html(f'<h5>{row}</h5>')
            st.markdown(f'''
                <table class="table table-bordered">
                    <thead class="table-light">
                        <tr>
                            <th style="width: 70% ;">Sumberdana</th>
                            <th style="width: 10% ;">Sebelum</th>
                            <th style="width: 10% ;">Sesudah</th>
                            <th style="width: 10% ;">Selisih</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{sumberdana}</td>
                            <td>{jumlahDanaSebelum}</td>
                            <td>{jumlahDanaSesudah}</td>
                            <td>{locale.format_string(
                "%d", jumlahDanaSelisih, grouping=True)}</td>
                        </tr>
                    </tbody>
                </table>
                <br />
                <br />
            ''', unsafe_allow_html=True)
    else:
        st.write(skpd)
else:
    skpd = df_copy
    dataRenjaSkpd = df_copy['SKPD'].unique()
    tableOpen = '''
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Uraian</th>
                <th>Sebelum</th>
                <th>Sesudah</th>
                <th>Selisih</th>
            </tr>
        </thead>
        <tbody>
    '''
    tableContent = f'''<tr>
                        <td>TOTAL</td>
                        <td>{locale.format_string("%d", skpd['JUMLAH'].sum(), grouping=True)}</td>
                        <td>{locale.format_string("%d", skpd['JUMLAH PERUBAHAN'].sum(), grouping=True)}</td>
                        <td>{locale.format_string("%d", skpd['JUMLAH PERUBAHAN'].sum() - skpd['JUMLAH'].sum(), grouping=True)}</td>
                    </tr>'''
    for opd in dataRenjaSkpd:
        tableContent += f'''<tr>
                        <td>{opd}</td>
                        <td>{locale.format_string("%d", skpd[skpd['SKPD'] == opd]['JUMLAH'].sum(), grouping=True)}</td>
                        <td>{locale.format_string("%d", skpd[skpd['SKPD'] == opd]['JUMLAH PERUBAHAN'].sum(), grouping=True)}</td>
                        <td>{locale.format_string("%d", skpd[skpd['SKPD'] == opd]['JUMLAH PERUBAHAN'].sum() - skpd[skpd['SKPD'] == opd]['JUMLAH'].sum(), grouping=True)}</td>
                    </tr>'''
    tableClose = '''</tbody></table><br />'''

    st.html('<h5>REKAP PER OPD</h5>')
    st.markdown(tableOpen + tableContent + tableClose, unsafe_allow_html=True)
    st.html('<h5>PROGRAM KGIATAN SEMUA SKPD</h5>')
    st.write(skpd)
