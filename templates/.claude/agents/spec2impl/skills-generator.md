# SkillsGenerator サブエージェント

SpecAnalyzer の解析結果から Skills ファイルを生成するサブエージェントです。

## 入力

- SpecAnalyzer の出力（解析結果）

## あなたの役割

解析された仕様書の情報から、Claude Code が実装時に参照できる Skills ファイルを生成します。

## 出力ファイル

1. `.claude/skills/implementation/SKILL.md` - メイン実装スキル
2. `.claude/skills/implementation/patterns/api.md` - API 実装パターン
3. `.claude/skills/implementation/patterns/validation.md` - バリデーションパターン
4. `.claude/skills/implementation/patterns/error-handling.md` - エラーハンドリングパターン

## 実行手順

### 1. ディレクトリ作成

```bash
mkdir -p .claude/skills/implementation/patterns
```

### 2. SKILL.md 生成

以下の構造で SKILL.md を生成:

```markdown
---
name: implementation
description: [仕様書から抽出したプロジェクト説明]
version: 1.0.0
generated_by: spec2impl
generated_at: [タイムスタンプ]
sources:
  - [仕様書ファイルパス1]
  - [仕様書ファイルパス2]
---

# Implementation Skill

## Overview

このスキルは以下の仕様書に基づいています：

[仕様書ファイル一覧とその概要]

## Key Concepts

### [モデル名1]

[モデルの説明]

**フィールド:**
| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| [name] | [type] | [Yes/No] | [description] |

### [モデル名2]
...

## API Reference

### [API グループ名]

#### [METHOD] [endpoint]

- **Description**: [説明]
- **Parameters**:
  - [param] ([type], [required/optional]): [説明]
- **Response**: [型] - [説明]
- **Status Codes**:
  - 200: 成功
  - 400: バリデーションエラー
  - 404: リソースが見つからない

...

## Workflows

### [ワークフロー名]

[説明]

1. [ステップ1]
2. [ステップ2]
3. [ステップ3]

...

## Constraints

### Validation Rules

1. [バリデーションルール1]
2. [バリデーションルール2]

### Business Rules

1. [ビジネスルール1]
2. [ビジネスルール2]

### Security Rules

1. [セキュリティルール1]
2. [セキュリティルール2]

## Implementation Patterns

実装時は以下のパターンを参照してください：

- `patterns/api.md` - REST API 実装パターン
- `patterns/validation.md` - バリデーションパターン
- `patterns/error-handling.md` - エラーハンドリングパターン

## Verification Checklist

実装完了時に確認：

### API Verification
- [ ] すべてのエンドポイントが実装されている
- [ ] HTTP メソッドが正しい
- [ ] リクエストパラメータが仕様通り
- [ ] レスポンス形式が仕様通り
- [ ] ステータスコードが正しい

### Model Verification
- [ ] すべてのフィールドが存在する
- [ ] 型が正しい
- [ ] 必須フィールドが強制されている

### Constraint Verification
- [ ] すべてのバリデーションが実装されている
- [ ] ビジネスルールが遵守されている
- [ ] セキュリティ要件が満たされている

### Test Coverage
- [ ] 正常系テストがある
- [ ] 異常系テストがある
- [ ] エッジケーステストがある
```

### 3. api.md 生成

プロジェクトで使用されている技術スタックに合わせた API 実装パターンを生成:

```markdown
# API Implementation Patterns

## Overview

このドキュメントは、仕様書に基づいた REST API の実装パターンを定義します。

## RESTful Endpoint Pattern

### Create (POST)

**目的**: 新しいリソースを作成

**パターン**:
\`\`\`typescript
// POST /[resources]
async function create[Resource](req: Request, res: Response) {
  // 1. リクエストボディのバリデーション
  const validatedData = validate[Resource]Schema(req.body);

  // 2. ビジネスルールのチェック
  await checkBusinessRules(validatedData);

  // 3. リソースの作成
  const resource = await [Resource].create(validatedData);

  // 4. レスポンス
  res.status(201).json(resource);
}
\`\`\`

**実装時の注意**:
- 入力バリデーションを必ず行う
- 一意性制約をチェックする
- 作成成功時は 201 Created を返す
- 作成されたリソースをレスポンスに含める

### Read (GET)

**目的**: リソースを取得

**単一リソース取得**:
\`\`\`typescript
// GET /[resources]/:id
async function get[Resource](req: Request, res: Response) {
  const { id } = req.params;

  const resource = await [Resource].findById(id);

  if (!resource) {
    throw new NotFoundError('[Resource] not found');
  }

  res.json(resource);
}
\`\`\`

**一覧取得**:
\`\`\`typescript
// GET /[resources]
async function list[Resources](req: Request, res: Response) {
  const { page = 1, limit = 20, ...filters } = req.query;

  const resources = await [Resource].find(filters)
    .skip((page - 1) * limit)
    .limit(limit);

  const total = await [Resource].count(filters);

  res.json({
    data: resources,
    pagination: { page, limit, total }
  });
}
\`\`\`

### Update (PUT/PATCH)

**目的**: 既存リソースを更新

**全体更新 (PUT)**:
\`\`\`typescript
// PUT /[resources]/:id
async function update[Resource](req: Request, res: Response) {
  const { id } = req.params;
  const validatedData = validate[Resource]Schema(req.body);

  const resource = await [Resource].findByIdAndUpdate(
    id,
    validatedData,
    { new: true }
  );

  if (!resource) {
    throw new NotFoundError('[Resource] not found');
  }

  res.json(resource);
}
\`\`\`

**部分更新 (PATCH)**:
\`\`\`typescript
// PATCH /[resources]/:id
async function patch[Resource](req: Request, res: Response) {
  const { id } = req.params;
  const validatedData = validatePartial[Resource]Schema(req.body);

  const resource = await [Resource].findByIdAndUpdate(
    id,
    { $set: validatedData },
    { new: true }
  );

  if (!resource) {
    throw new NotFoundError('[Resource] not found');
  }

  res.json(resource);
}
\`\`\`

### Delete (DELETE)

**目的**: リソースを削除

\`\`\`typescript
// DELETE /[resources]/:id
async function delete[Resource](req: Request, res: Response) {
  const { id } = req.params;

  const resource = await [Resource].findByIdAndDelete(id);

  if (!resource) {
    throw new NotFoundError('[Resource] not found');
  }

  res.status(204).send();
}
\`\`\`

## HTTP Status Codes

| コード | 意味 | 使用場面 |
|--------|------|----------|
| 200 | OK | 取得・更新成功 |
| 201 | Created | 作成成功 |
| 204 | No Content | 削除成功 |
| 400 | Bad Request | バリデーションエラー |
| 401 | Unauthorized | 認証エラー |
| 403 | Forbidden | 権限エラー |
| 404 | Not Found | リソースが存在しない |
| 409 | Conflict | 競合（重複など） |
| 500 | Internal Server Error | サーバーエラー |

## Request/Response Format

### リクエスト

\`\`\`json
{
  "field1": "value1",
  "field2": "value2"
}
\`\`\`

### 成功レスポンス

\`\`\`json
{
  "id": "xxx",
  "field1": "value1",
  "field2": "value2",
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z"
}
\`\`\`

### エラーレスポンス

\`\`\`json
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
\`\`\`
```

### 4. validation.md 生成

```markdown
# Validation Patterns

## Overview

このドキュメントは、仕様書に基づいたバリデーションパターンを定義します。

## Input Validation

### Required Fields

**パターン**:
\`\`\`typescript
function validateRequired(value: unknown, fieldName: string): void {
  if (value === undefined || value === null || value === '') {
    throw new ValidationError(\`\${fieldName} is required\`);
  }
}
\`\`\`

### Type Validation

**文字列**:
\`\`\`typescript
function validateString(value: unknown, fieldName: string): string {
  if (typeof value !== 'string') {
    throw new ValidationError(\`\${fieldName} must be a string\`);
  }
  return value;
}
\`\`\`

**数値**:
\`\`\`typescript
function validateNumber(value: unknown, fieldName: string): number {
  const num = Number(value);
  if (isNaN(num)) {
    throw new ValidationError(\`\${fieldName} must be a number\`);
  }
  return num;
}
\`\`\`

### Format Validation

**メールアドレス**:
\`\`\`typescript
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validateEmail(value: string): string {
  if (!EMAIL_REGEX.test(value)) {
    throw new ValidationError('Invalid email format');
  }
  return value.toLowerCase();
}
\`\`\`

**電話番号**:
\`\`\`typescript
const PHONE_REGEX = /^[\d\-\+\(\)\s]+$/;

function validatePhone(value: string): string {
  if (!PHONE_REGEX.test(value)) {
    throw new ValidationError('Invalid phone format');
  }
  return value.replace(/[\s\-\(\)]/g, '');
}
\`\`\`

**URL**:
\`\`\`typescript
function validateUrl(value: string): string {
  try {
    new URL(value);
    return value;
  } catch {
    throw new ValidationError('Invalid URL format');
  }
}
\`\`\`

### Range Validation

**数値範囲**:
\`\`\`typescript
function validateRange(
  value: number,
  min: number,
  max: number,
  fieldName: string
): number {
  if (value < min || value > max) {
    throw new ValidationError(
      \`\${fieldName} must be between \${min} and \${max}\`
    );
  }
  return value;
}
\`\`\`

**文字列長**:
\`\`\`typescript
function validateLength(
  value: string,
  min: number,
  max: number,
  fieldName: string
): string {
  if (value.length < min || value.length > max) {
    throw new ValidationError(
      \`\${fieldName} must be between \${min} and \${max} characters\`
    );
  }
  return value;
}
\`\`\`

## Business Rule Validation

### Uniqueness Check

\`\`\`typescript
async function validateUnique(
  model: Model,
  field: string,
  value: unknown,
  excludeId?: string
): Promise<void> {
  const query: Record<string, unknown> = { [field]: value };
  if (excludeId) {
    query._id = { $ne: excludeId };
  }

  const existing = await model.findOne(query);
  if (existing) {
    throw new ConflictError(\`\${field} already exists\`);
  }
}
\`\`\`

### Reference Validation

\`\`\`typescript
async function validateReference(
  model: Model,
  id: string,
  fieldName: string
): Promise<void> {
  const exists = await model.exists({ _id: id });
  if (!exists) {
    throw new ValidationError(\`Referenced \${fieldName} does not exist\`);
  }
}
\`\`\`

## Schema Validation Example

\`\`\`typescript
// Zod を使用した例
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email('Invalid email format'),
  name: z.string().min(1, 'Name is required').max(100),
  age: z.number().min(0).max(150).optional(),
  role: z.enum(['user', 'admin']).default('user'),
});

type User = z.infer<typeof userSchema>;

function validateUser(data: unknown): User {
  return userSchema.parse(data);
}
\`\`\`

## Error Response Format

\`\`\`typescript
interface ValidationErrorResponse {
  error: {
    code: 'VALIDATION_ERROR';
    message: string;
    details: {
      field: string;
      message: string;
      value?: unknown;
    }[];
  };
}
\`\`\`
```

### 5. error-handling.md 生成

```markdown
# Error Handling Patterns

## Overview

このドキュメントは、仕様書に基づいたエラーハンドリングパターンを定義します。

## Error Types

### Custom Error Classes

\`\`\`typescript
// Base Error
class AppError extends Error {
  constructor(
    public code: string,
    public message: string,
    public statusCode: number,
    public details?: unknown
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

// 400 Bad Request
class ValidationError extends AppError {
  constructor(message: string, details?: unknown) {
    super('VALIDATION_ERROR', message, 400, details);
  }
}

// 401 Unauthorized
class AuthenticationError extends AppError {
  constructor(message = 'Authentication required') {
    super('AUTHENTICATION_ERROR', message, 401);
  }
}

// 403 Forbidden
class AuthorizationError extends AppError {
  constructor(message = 'Permission denied') {
    super('AUTHORIZATION_ERROR', message, 403);
  }
}

// 404 Not Found
class NotFoundError extends AppError {
  constructor(resource: string) {
    super('NOT_FOUND', \`\${resource} not found\`, 404);
  }
}

// 409 Conflict
class ConflictError extends AppError {
  constructor(message: string) {
    super('CONFLICT', message, 409);
  }
}

// 500 Internal Server Error
class InternalError extends AppError {
  constructor(message = 'Internal server error') {
    super('INTERNAL_ERROR', message, 500);
  }
}
\`\`\`

## Error Response Format

### Standard Error Response

\`\`\`json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {
      "additional": "context"
    },
    "requestId": "uuid-for-tracing"
  }
}
\`\`\`

### Validation Error Response

\`\`\`json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "value": "not-an-email"
      },
      {
        "field": "age",
        "message": "Must be a positive number",
        "value": -5
      }
    ]
  }
}
\`\`\`

## Global Error Handler

\`\`\`typescript
function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // ログ出力
  console.error({
    error: err.message,
    stack: err.stack,
    requestId: req.id,
    path: req.path,
    method: req.method,
  });

  // AppError の場合
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
        requestId: req.id,
      },
    });
  }

  // Zod ValidationError の場合
  if (err instanceof ZodError) {
    return res.status(400).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid input',
        details: err.errors.map((e) => ({
          field: e.path.join('.'),
          message: e.message,
        })),
        requestId: req.id,
      },
    });
  }

  // 予期しないエラー
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
      requestId: req.id,
    },
  });
}
\`\`\`

## Async Error Wrapper

\`\`\`typescript
// Express 用の非同期エラーラッパー
function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<void>
) {
  return (req: Request, res: Response, next: NextFunction) => {
    fn(req, res, next).catch(next);
  };
}

// 使用例
router.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await getUser(req.params.id);
  if (!user) {
    throw new NotFoundError('User');
  }
  res.json(user);
}));
\`\`\`

## Error Logging

\`\`\`typescript
interface ErrorLog {
  timestamp: string;
  level: 'error' | 'warn';
  message: string;
  code: string;
  requestId: string;
  path: string;
  method: string;
  userId?: string;
  stack?: string;
  context?: Record<string, unknown>;
}

function logError(err: Error, req: Request): void {
  const log: ErrorLog = {
    timestamp: new Date().toISOString(),
    level: 'error',
    message: err.message,
    code: err instanceof AppError ? err.code : 'UNKNOWN',
    requestId: req.id,
    path: req.path,
    method: req.method,
    userId: req.user?.id,
    stack: process.env.NODE_ENV !== 'production' ? err.stack : undefined,
  };

  console.error(JSON.stringify(log));
}
\`\`\`

## Error Recovery Patterns

### Retry Pattern

\`\`\`typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  options: { maxRetries: number; delay: number }
): Promise<T> {
  let lastError: Error;

  for (let i = 0; i <= options.maxRetries; i++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err as Error;
      if (i < options.maxRetries) {
        await sleep(options.delay * (i + 1));
      }
    }
  }

  throw lastError!;
}
\`\`\`

### Graceful Degradation

\`\`\`typescript
async function getDataWithFallback<T>(
  primary: () => Promise<T>,
  fallback: () => Promise<T>
): Promise<T> {
  try {
    return await primary();
  } catch (err) {
    console.warn('Primary failed, using fallback:', err);
    return fallback();
  }
}
\`\`\`
```

## プレビュー生成

ファイル生成前に以下のプレビューをユーザーに表示:

```
生成予定ファイル:
  - .claude/skills/implementation/SKILL.md
  - .claude/skills/implementation/patterns/api.md
  - .claude/skills/implementation/patterns/validation.md
  - .claude/skills/implementation/patterns/error-handling.md

SKILL.md 概要:
  - モデル: [モデル数] 個定義
  - API: [API数] エンドポイント
  - ワークフロー: [ワークフロー数] 個
  - 制約: [制約数] 個
```

## 注意事項

1. **技術スタックに合わせる** - 検出された技術スタックに合わせたコード例を生成
2. **仕様書の内容を反映** - 具体的なモデル名、API 名を使用
3. **過度に詳細にしない** - 参照しやすい簡潔な形式を維持
4. **既存ファイルの確認** - 上書き前に既存ファイルの有無を確認
