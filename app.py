import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="🎓",
    layout="wide"
)

# ==============================
# 1. DỮ LIỆU 10 SINH VIÊN
# ==============================
data = {
    "Họ tên": [
        "An", "Bình", "Chi", "Dũng", "Hà",
        "Lan", "Minh", "Nam", "Phúc", "Trang"
    ],
    "Chuyên cần": [8, 9, 7, 10, 8, 7, 9, 8, 8, 10],
    "Giữa kỳ": [7, 8, 6, 9, 7, 6, 8, 7, 8, 9],
    "Cuối kỳ": [8, 8.5, 6.5, 9.5, 7.5, 6, 9, 7.5, 8, 9]
}

df = pd.DataFrame(data)

# ==============================
# 2. TÍNH ĐIỂM TỔNG KẾT
# 20% chuyên cần + 30% giữa kỳ + 50% cuối kỳ
# ==============================
df["Tổng kết"] = (
    0.2 * df["Chuyên cần"]
    + 0.3 * df["Giữa kỳ"]
    + 0.5 * df["Cuối kỳ"]
)

# ==============================
# 3. XẾP LOẠI
# ==============================
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# ==============================
# 4. THỐNG KÊ
# ==============================
diem_tb = df["Tổng kết"].mean()
sv_cao_nhat = df.loc[df["Tổng kết"].idxmax()]
sv_thap_nhat = df.loc[df["Tổng kết"].idxmin()]
so_sv_dat = int((df["Tổng kết"] >= 5).sum())

# ==============================
# 5. TIÊU ĐỀ
# ==============================
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Ứng dụng quản lý điểm sinh viên bằng Python, Pandas và Streamlit.")

# ==============================
# 6. BẢNG ĐIỂM
# ==============================
st.subheader("📋 Bảng điểm 10 sinh viên")
st.dataframe(
    df.style.format({
        "Chuyên cần": "{:.1f}",
        "Giữa kỳ": "{:.1f}",
        "Cuối kỳ": "{:.1f}",
        "Tổng kết": "{:.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

# ==============================
# 7. THỐNG KÊ
# ==============================
st.subheader("📊 Thống kê")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Điểm trung bình", f"{diem_tb:.2f}")
c2.metric("Điểm cao nhất", f"{sv_cao_nhat['Tổng kết']:.2f}")
c3.metric("Điểm thấp nhất", f"{sv_thap_nhat['Tổng kết']:.2f}")
c4.metric("Số sinh viên đạt", f"{so_sv_dat}/10")

st.info(
    f"Sinh viên cao nhất: **{sv_cao_nhat['Họ tên']}** "
    f"({sv_cao_nhat['Tổng kết']:.2f})"
)

st.warning(
    f"Sinh viên thấp nhất: **{sv_thap_nhat['Họ tên']}** "
    f"({sv_thap_nhat['Tổng kết']:.2f})"
)

# ==============================
# 8. CHỌN SINH VIÊN
# ==============================
st.subheader("🔎 Tra cứu thông tin sinh viên")

selected_name = st.selectbox(
    "Chọn một sinh viên:",
    df["Họ tên"].tolist()
)

student = df[df["Họ tên"] == selected_name].iloc[0]

a, b, c = st.columns(3)

a.write(f"**Chuyên cần:** {student['Chuyên cần']:.1f}")
a.write(f"**Giữa kỳ:** {student['Giữa kỳ']:.1f}")

b.write(f"**Cuối kỳ:** {student['Cuối kỳ']:.1f}")
b.write(f"**Tổng kết:** {student['Tổng kết']:.2f}")

c.write(f"**Xếp loại:** {student['Xếp loại']}")

# ==============================
# 9. BIỂU ĐỒ
# ==============================
st.subheader("📈 Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df["Họ tên"], df["Tổng kết"])
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.grid(axis="y", alpha=0.25)

plt.xticks(rotation=30)
plt.tight_layout()

st.pyplot(fig)

# ==============================
# 10. THÔNG TIN NGƯỜI TẠO
# ==============================
st.markdown("---")
st.caption("Ứng dụng được tạo bởi: HỌ VÀ TÊN - MSSV")
