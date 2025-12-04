# User Management API 仕様書

## 概要

ユーザー管理機能を提供する REST API です。

## 技術スタック

- Framework: Express.js + TypeScript
- Database: PostgreSQL
- Authentication: JWT

---

## データモデル

### User

ユーザー情報を表すモデルです。

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string (UUID) | Yes | ユーザーの一意識別子 |
| email | string | Yes | メールアドレス（一意） |
| name | string | Yes | 表示名 |
| password | string | Yes | ハッシュ化されたパスワード |
| role | enum | Yes | ユーザーロール（user, admin） |
| createdAt | datetime | Yes | 作成日時 |
| updatedAt | datetime | Yes | 更新日時 |

### UserProfile

ユーザーのプロフィール情報です。

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| userId | string (UUID) | Yes | ユーザーID（外部キー） |
| avatar | string | No | アバター画像URL |
| bio | string | No | 自己紹介（最大500文字） |
| website | string | No | WebサイトURL |

---

## API エンドポイント

### ユーザー作成

#### POST /api/users

新規ユーザーを作成します。

**Request Body:**

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "securePassword123"
}
```

**Parameters:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| email | string | Yes | メールアドレス |
| name | string | Yes | 表示名（1-100文字） |
| password | string | Yes | パスワード（8文字以上） |

**Response:**

- `201 Created`: ユーザー作成成功

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

- `400 Bad Request`: バリデーションエラー
- `409 Conflict`: メールアドレスが既に存在

---

### ユーザー取得

#### GET /api/users/:id

指定されたIDのユーザーを取得します。

**Parameters:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string (path) | Yes | ユーザーID |

**Response:**

- `200 OK`: 成功

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z"
}
```

- `404 Not Found`: ユーザーが存在しない

---

### ユーザー一覧取得

#### GET /api/users

ユーザー一覧を取得します（ページネーション対応）。

**Query Parameters:**

| パラメータ | 型 | 必須 | デフォルト | 説明 |
|-----------|-----|------|-----------|------|
| page | number | No | 1 | ページ番号 |
| limit | number | No | 20 | 1ページあたりの件数（最大100） |
| role | string | No | - | ロールでフィルタ |

**Response:**

- `200 OK`: 成功

```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "name": "John Doe",
      "role": "user"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

---

### ユーザー更新

#### PUT /api/users/:id

ユーザー情報を更新します。

**Parameters:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string (path) | Yes | ユーザーID |

**Request Body:**

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Response:**

- `200 OK`: 更新成功
- `400 Bad Request`: バリデーションエラー
- `404 Not Found`: ユーザーが存在しない
- `409 Conflict`: メールアドレスが既に使用されている

---

### ユーザー削除

#### DELETE /api/users/:id

ユーザーを削除します（論理削除）。

**Parameters:**

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | string (path) | Yes | ユーザーID |

**Response:**

- `204 No Content`: 削除成功
- `404 Not Found`: ユーザーが存在しない

---

## 制約・ビジネスルール

### バリデーションルール

1. メールアドレスは有効な形式であること
2. メールアドレスはシステム内で一意であること
3. パスワードは8文字以上であること
4. パスワードは大文字、小文字、数字を含むこと
5. 表示名は1-100文字であること

### ビジネスルール

1. ユーザー削除は論理削除とする
2. 管理者（admin）のみが他ユーザーの役割を変更できる
3. 自分自身のアカウントは削除できない

### セキュリティルール

1. パスワードはbcryptでハッシュ化して保存
2. APIはJWT認証が必要（一部を除く）
3. パスワードはレスポンスに含めない

---

## ワークフロー

### ユーザー登録フロー

1. クライアントがPOST /api/usersにリクエスト
2. サーバーがメールアドレスの重複をチェック
3. パスワードをハッシュ化
4. ユーザーレコードを作成
5. 確認メールを送信（非同期）
6. 作成されたユーザー情報を返却

### パスワードリセットフロー

1. ユーザーがメールアドレスを入力
2. リセットトークンを生成（有効期限: 1時間）
3. リセットリンクをメール送信
4. ユーザーが新しいパスワードを設定
5. トークンを無効化

---

## エラーレスポンス形式

すべてのエラーは以下の形式で返却されます：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### エラーコード一覧

| コード | HTTP Status | 説明 |
|--------|-------------|------|
| VALIDATION_ERROR | 400 | 入力バリデーションエラー |
| UNAUTHORIZED | 401 | 認証が必要 |
| FORBIDDEN | 403 | 権限がない |
| NOT_FOUND | 404 | リソースが見つからない |
| CONFLICT | 409 | 競合（重複など） |
| INTERNAL_ERROR | 500 | サーバーエラー |

---

## Implementation Checklist

- [ ] User モデルの実装
- [ ] UserProfile モデルの実装
- [ ] POST /api/users エンドポイント
- [ ] GET /api/users/:id エンドポイント
- [ ] GET /api/users エンドポイント（一覧）
- [ ] PUT /api/users/:id エンドポイント
- [ ] DELETE /api/users/:id エンドポイント
- [ ] バリデーションミドルウェア
- [ ] 認証ミドルウェア
- [ ] エラーハンドリング
- [ ] ユニットテスト
- [ ] 統合テスト

## Verification Checklist

- [ ] すべてのエンドポイントが実装されている
- [ ] バリデーションが仕様通りに動作する
- [ ] エラーレスポンスが仕様に準拠している
- [ ] パスワードがハッシュ化されている
- [ ] レスポンスにパスワードが含まれていない
- [ ] ページネーションが正しく動作する
- [ ] 認証が必要なエンドポイントで認証チェックが行われる
