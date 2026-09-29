# EduGenie API

## GET `/health`

Returns service status.

## POST `/qa`

Request:

```json
{
  "question": "What is an algorithm?",
  "context": "Optional supporting context"
}
```

## POST `/explain`

Request:

```json
{
  "topic": "Pythagoras theorem",
  "level": "beginner"
}
```

## POST `/quiz`

Request:

```json
{
  "text": "Educational passage",
  "topic": "Optional topic"
}
```

Response contains exactly three questions, each with four options.

## POST `/summarize`

Request:

```json
{
  "text": "Long educational passage",
  "max_words": 120
}
```

## POST `/learn/recommendations`

Request:

```json
{
  "topic": "SQL",
  "level": "beginner",
  "goal": "Become job-ready"
}
```

The quiz and learning-path responses are schema-validated Pydantic objects.
