# Ảnh Chi Nhận Linh · Website mẫu PBZ Việt

Đây là bản mẫu website tĩnh, viết bằng HTML/CSS/JavaScript và có thể xuất bản miễn phí bằng GitHub Pages.

## Chức năng đã có
- Toàn bộ nhãn giao diện bằng tiếng Việt.
- Giao diện gọn gàng tương thích điện thoại.
- Tìm kiếm tên Hán–Việt, chữ Hán, tiếng Anh và mô tả.
- Phân loại độ tin cậy A/B/C và liên kết nguồn.
- Danh mục nguồn; trang hiển thị URL đã thay đổi.
- GitHub Actions kiểm tra thay đổi ba URL công khai theo lịch; ngày đầu chỉ ghi mốc.
- Bảng từ điển Hán–Việt tách riêng.

## Chưa có (cần bước tiếp theo)
- Tự động tải và dịch các bài viết mới qua AI.
- Tự động điền hàng trăm boss/vũ khí và kiểm duyệt nội dung.
- Xuất bản tự động sau khi kiểm chứng.
- Đồng bộ thông báo trong ChatGPT với nội dung trên GitHub. Đây là hai cơ chế độc lập.

## Hướng dẫn đưa lên GitHub Pages
1. Đề nghị tạo repository Public mới tên `pbz-viet` để không làm mất website `anh-chi-nhan` hiện tại.
2. Giải nén gói ZIP. Trên GitHub > repo mới > **Add file > Upload files**. Kéo nội dung BÊN TRONG thư mục được giải nén lên GitHub. Kiểm tra giữ đủ thư mục `assets`, `data`, `scripts`, `state` và `.github/workflows` rồi nhấn **Commit changes**. Nếu trình tải web không nhận thư mục ẩn `.github`, tạo file bằng **Add file > Create new file**, đặt tên `.github/workflows/pages.yml` và dán nội dung trong ZIP.
3. Repo > **Settings > Pages > Source > GitHub Actions**.
4. Mở tab **Actions**, cho phép Actions nếu GitHub hỏi, chạy workflow `Xuat ban web va kiem tra nguon` > **Run workflow**.
5. Chờ bước deploy hiển thị hoàn tất, lấy URL trong Settings > Pages. Thường là `https://USERNAME.github.io/pbz-viet/`.
6. Thêm thông tin mới bằng cách sửa `data/entries.json` hoặc `data/sources.json`. Những thay đổi phải được xác thực và diễn giải riêng.

## Biên tập
- `data/entries.json`: mục hiển thị trong thư viện. Các trường id, category, hv, zh, en, description, level và source_url.
- `data/glossary.json`: cách viết chuẩn tên Hán–Việt.
- `data/sources.json`: danh sách nguồn công khai để người đọc đối chiếu.
- `scripts/check_sources.py`: danh sách URL kiểm tra trong `WATCH`. Chỉ thêm trang sau khi tự kiểm tra điều khoản, robots và quyền truy cập tự động.
- `data/updates.json`: lịch sử URL bị thay đổi. Không phải bài viết mới đã được dịch.
- `state/source_state.json`: dấu vân tay nội dung phục vụ so sánh.

## Lưu ý
- Giới thiệu game, tên riêng và mô tả do tác giả bản mẫu biên tập; không mặc nhiên là tên chính thức tiếng Việt.
- Không sao chép toàn bộ nội dung/hình ảnh từ các trang bên thứ ba nếu chưa được cho phép.
- Một số nguồn có thể chống bot, thay đổi HTML hoặc cấm thu thập; script sẽ kiểm tra robots.txt trước. Nếu không xác minh được robots hoặc không lấy được HTML, workflow chỉ ghi lỗi và không vượt qua rào chắn.
- Việc GitHub Actions được chạy định kỳ có thể bị chậm, lỗi hoặc ngừng do giới hạn nền tảng; cần kiểm tra tab Actions.
- Không đưa API key vào file trong repository Public. Khi tích hợp AI sau này phải sử dụng **Settings > Secrets and variables > Actions**.
- Có thể xem trực tiếp file HTML bằng máy, nhưng tính năng tải JSON cần một máy chủ web, chẳng hạn GitHub Pages (file:// sẽ không hoạt động).
