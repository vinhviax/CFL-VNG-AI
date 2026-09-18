# Thuật ngữ vũ khí — CrossFire Legends VN

> **Phiên bản:** draft-01 · **Trạng thái:** draft · **Hiệu lực:** chưa chốt
> **Mức:** P3 nội bộ phổ biến · **Chủ sở hữu:** *chưa gán* · **Nguồn:** `01_weapons_usage.csv` (1227 dòng) + `02_weapon_name_map.csv` (2599 dòng), trích 15/08/2026


Trang này định nghĩa bộ từ vựng chuẩn để gọi tên vũ khí. Mọi nội dung gửi người chơi phải dùng đúng thuật ngữ ở đây, không tự đặt tên mới.


## Quy tắc đặt tên vũ khí

Tên hiển thị theo cấu trúc `<Dòng súng>-<Dòng skin>-<Bậc>`:

```text
AK47-Beast-Noble Gold
│    │     └── Bậc
│    └──────── Dòng skin
└───────────── Dòng súng
```

Không phải mọi tên đều đủ ba phần. Tên chỉ có hai phần (`AK47-Beast`) là bản gốc chưa nâng bậc.


## Loại vũ khí — 8 giá trị chuẩn

| Thuật ngữ chuẩn (EN) | Gọi trong nội dung tiếng Việt | Số mục |
|---|---|---:|
| `Rifle` | súng trường | 456 |
| `Secondary` | vũ khí phụ | 217 |
| `Melee` | vũ khí cận chiến | 155 |
| `Sniper` | súng bắn tỉa | 113 |
| `Utility` | vật phẩm hỗ trợ | 84 |
| `SMG` | tiểu liên | 82 |
| `Shotgun` | súng ngắn nòng | 64 |
| `Machine Gun` | súng máy | 56 |

## Dòng súng — 12 giá trị

Trường `fam` **đang dùng tiếng Việt lẫn tên mã**, cần chuẩn hoá:

| Giá trị trong dữ liệu | Ghi chú |
|---|---|
| `Súng lục` | nhóm gộp tiếng Việt |
| `Súng trường khác` | nhóm gộp tiếng Việt |
| `Cận chiến` | nhóm gộp tiếng Việt |
| `AK47` | tên mã cụ thể, giữ nguyên |
| `M4A1` | tên mã cụ thể, giữ nguyên |
| `SMG` | tên mã cụ thể, giữ nguyên |
| `Đặc biệt` | nhóm gộp tiếng Việt |
| `Shotgun` | tên mã cụ thể, giữ nguyên |
| `Bắn tỉa khác` | nhóm gộp tiếng Việt |
| `AWM` | tên mã cụ thể, giữ nguyên |
| `Barrett` | tên mã cụ thể, giữ nguyên |
| `M200` | tên mã cụ thể, giữ nguyên |

## Bậc phẩm chất — 14 giá trị, **có lỗi dữ liệu**

| Giá trị trong dữ liệu | Số mục | Trạng thái |
|---|---:|---|
| `Purple` | 354 | hợp lệ |
| `Gold V` | 240 | hợp lệ |
| `Orange` | 195 | hợp lệ |
| `Gold VVIP` | 158 | hợp lệ |
| `C` | 52 | ⚠️ hệ ký tự, không cùng hệ màu — cần thống nhất |
| `Blue` | 52 | hợp lệ |
| `B` | 36 | ⚠️ hệ ký tự, không cùng hệ màu — cần thống nhất |
| `Green` | 34 | hợp lệ |
| `Red` | 24 | hợp lệ |
| `` | 24 | ⚠️ **rỗng** — cần điền |
| `Silver V` | 22 | hợp lệ |
| `Whtie` | 15 | ❌ **sai chính tả**, phải là `White` |
| `A` | 12 | ⚠️ hệ ký tự, không cùng hệ màu — cần thống nhất |
| `Limited` | 9 | hợp lệ |

**Phải xử lý trước khi nạp KB:** sửa `Whtie` → `White`; điền 24 dòng phẩm chất rỗng; quyết định gộp hay tách hai hệ `A/B/C` và hệ màu.


## Dòng skin — 485 giá trị

Top 20 theo số biến thể. Danh sách đầy đủ sinh lại từ `02_weapon_name_map.csv`.

| Dòng skin | Số biến thể |
|---|---:|
| Born Beast | 169 |
| Beast | 96 |
| Iron Beast | 91 |
| Predator | 44 |
| Gold | 34 |
| Ranger | 25 |
| Winter Land | 25 |
| Angel | 24 |
| Infernal Dragon | 22 |
| Iron Shark | 17 |
| S | 17 |
| A | 16 |
| Mechanical Era | 15 |
| Royal Dragon | 13 |
| Dragon | 12 |
| Tournament Spirit | 12 |
| Armoured Beast | 11 |
| Titanium Beast | 11 |
| El Dorado | 10 |
| Gaming Glory | 10 |

## Chưa có, cần bổ sung

- Tên tiếng Việt chính thức của từng dòng skin — hiện chỉ có tiếng Anh
- Tên tiếng Trung đối chiếu (nguồn từ bản gốc)
- Thuật ngữ hệ thống ngoài vũ khí: chế độ chơi, tiền tệ, sự kiện, giao diện
- Quy tắc viết hoa và cách chèn tên vũ khí vào câu tiếng Việt
