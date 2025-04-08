# hocvienai-API

API mô tả ảnh bằng GPT-4 Vision cho website hocvienai.click

## Endpoint

`POST /generate-prompt`

### Body:
- `file`: ảnh (form-data)

### Response:
```json
{
  "english": "Mô tả bằng tiếng Anh từ GPT-4",
  "vietnamese": "Mô tả dịch sang tiếng Việt"
}
```

## Biến môi trường cần có

- `OPENAI_API_KEY` (bắt buộc)
- `HF_TOKEN` (tùy chọn, dùng để dịch sang tiếng Việt)
