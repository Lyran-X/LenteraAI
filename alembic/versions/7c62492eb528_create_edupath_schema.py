"""create edupath schema

Revision ID: 7c62492eb528
Revises: 
Create Date: 2026-05-26 19:03:48.955853
"""

from typing import Sequence, Union

from alembic import op



revision: str = '7c62492eb528'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE EXTENSION IF NOT EXISTS pgcrypto;

        CREATE TYPE document_status AS ENUM ('uploaded', 'processing', 'ready', 'failed', 'archived');
        CREATE TYPE chat_session_type AS ENUM ('general_tutor', 'document_qa');
        CREATE TYPE chat_role AS ENUM ('system', 'user', 'assistant');
        CREATE TYPE study_plan_status AS ENUM ('draft', 'active', 'completed', 'archived');
        CREATE TYPE study_plan_item_type AS ENUM ('reading', 'practice', 'quiz', 'revision', 'project');
        CREATE TYPE study_plan_item_status AS ENUM ('todo', 'in_progress', 'done', 'skipped');
        CREATE TYPE quiz_source_type AS ENUM ('topic', 'document', 'mixed');
        CREATE TYPE quiz_status AS ENUM ('draft', 'published', 'archived');
        CREATE TYPE question_type AS ENUM ('multiple_choice', 'true_false', 'short_answer', 'essay');
        CREATE TYPE attempt_status AS ENUM ('in_progress', 'submitted', 'graded');
        CREATE TYPE note_source_type AS ENUM ('manual', 'ai_message', 'document', 'document_chunk', 'quiz_review');

        CREATE TABLE users (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          email TEXT NOT NULL,
          password_hash TEXT NOT NULL,
          full_name TEXT NOT NULL,
          avatar_url TEXT,
          role TEXT NOT NULL DEFAULT 'student',
          preferred_language VARCHAR(16) NOT NULL DEFAULT 'id',
          education_level TEXT,
          learning_goals TEXT[] NOT NULL DEFAULT '{}',
          timezone TEXT NOT NULL DEFAULT 'Asia/Jakarta',
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          last_login_at TIMESTAMPTZ,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          CONSTRAINT users_role_check CHECK (role IN ('student', 'admin')),
          CONSTRAINT users_email_not_blank CHECK (length(trim(email)) > 0)
        );

        CREATE TABLE uploaded_documents (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          title TEXT NOT NULL,
          original_filename TEXT NOT NULL,
          mime_type TEXT NOT NULL,
          file_size_bytes BIGINT NOT NULL CHECK (file_size_bytes >= 0),
          storage_provider TEXT NOT NULL DEFAULT 'local',
          storage_path TEXT NOT NULL,
          status document_status NOT NULL DEFAULT 'uploaded',
          page_count INTEGER CHECK (page_count IS NULL OR page_count >= 0),
          word_count INTEGER CHECK (word_count IS NULL OR word_count >= 0),
          summary TEXT,
          processed_at TIMESTAMPTZ,
          error_message TEXT,
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          UNIQUE (id, user_id)
        );

        CREATE TABLE document_chunks (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          document_id UUID NOT NULL,
          user_id UUID NOT NULL,
          chunk_index INTEGER NOT NULL CHECK (chunk_index >= 0),
          content TEXT NOT NULL,
          content_hash TEXT,
          token_count INTEGER CHECK (token_count IS NULL OR token_count >= 0),
          char_start INTEGER CHECK (char_start IS NULL OR char_start >= 0),
          char_end INTEGER CHECK (char_end IS NULL OR char_end >= 0),
          page_start INTEGER CHECK (page_start IS NULL OR page_start >= 0),
          page_end INTEGER CHECK (page_end IS NULL OR page_end >= 0),
          embedding_model TEXT,
          vector_store TEXT NOT NULL DEFAULT 'chroma',
          vector_collection TEXT,
          vector_id TEXT,
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          FOREIGN KEY (document_id, user_id)
            REFERENCES uploaded_documents(id, user_id)
            ON DELETE CASCADE,
          UNIQUE (document_id, chunk_index),
          CONSTRAINT document_chunks_char_range_check CHECK (
            char_start IS NULL OR char_end IS NULL OR char_end >= char_start
          ),
          CONSTRAINT document_chunks_page_range_check CHECK (
            page_start IS NULL OR page_end IS NULL OR page_end >= page_start
          )
        );

        CREATE TABLE ai_chat_sessions (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          document_id UUID REFERENCES uploaded_documents(id) ON DELETE SET NULL,
          title TEXT NOT NULL DEFAULT 'New Chat',
          session_type chat_session_type NOT NULL DEFAULT 'general_tutor',
          model_provider TEXT,
          model_name TEXT,
          system_prompt TEXT,
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          last_message_at TIMESTAMPTZ,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );

        CREATE TABLE ai_chat_messages (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          session_id UUID NOT NULL REFERENCES ai_chat_sessions(id) ON DELETE CASCADE,
          user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          sequence_number INTEGER NOT NULL CHECK (sequence_number >= 0),
          role chat_role NOT NULL,
          content TEXT NOT NULL,
          model_provider TEXT,
          model_name TEXT,
          prompt_tokens INTEGER CHECK (prompt_tokens IS NULL OR prompt_tokens >= 0),
          completion_tokens INTEGER CHECK (completion_tokens IS NULL OR completion_tokens >= 0),
          total_tokens INTEGER CHECK (total_tokens IS NULL OR total_tokens >= 0),
          latency_ms INTEGER CHECK (latency_ms IS NULL OR latency_ms >= 0),
          related_document_id UUID REFERENCES uploaded_documents(id) ON DELETE SET NULL,
          retrieval_query TEXT,
          citations JSONB NOT NULL DEFAULT '[]'::jsonb,
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          UNIQUE (session_id, sequence_number)
        );

        CREATE TABLE study_plans (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          title TEXT NOT NULL,
          description TEXT,
          goal TEXT,
          level TEXT,
          weekly_hours INTEGER CHECK (weekly_hours IS NULL OR weekly_hours >= 0),
          start_date DATE,
          end_date DATE,
          status study_plan_status NOT NULL DEFAULT 'draft',
          generated_by_ai BOOLEAN NOT NULL DEFAULT true,
          model_name TEXT,
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          CONSTRAINT study_plans_date_range_check CHECK (
            start_date IS NULL OR end_date IS NULL OR end_date >= start_date
          )
        );

        CREATE TABLE quizzes (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          source_type quiz_source_type NOT NULL DEFAULT 'topic',
          source_document_id UUID REFERENCES uploaded_documents(id) ON DELETE SET NULL,
          title TEXT NOT NULL,
          topic TEXT,
          description TEXT,
          difficulty TEXT NOT NULL DEFAULT 'medium',
          status quiz_status NOT NULL DEFAULT 'draft',
          time_limit_minutes INTEGER CHECK (time_limit_minutes IS NULL OR time_limit_minutes > 0),
          total_questions INTEGER NOT NULL DEFAULT 0 CHECK (total_questions >= 0),
          generated_by_ai BOOLEAN NOT NULL DEFAULT true,
          model_name TEXT,
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          CONSTRAINT quizzes_difficulty_check CHECK (difficulty IN ('easy', 'medium', 'hard', 'mixed'))
        );

        CREATE TABLE study_plan_items (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          study_plan_id UUID NOT NULL REFERENCES study_plans(id) ON DELETE CASCADE,
          user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          linked_document_id UUID REFERENCES uploaded_documents(id) ON DELETE SET NULL,
          linked_quiz_id UUID REFERENCES quizzes(id) ON DELETE SET NULL,
          title TEXT NOT NULL,
          description TEXT,
          item_type study_plan_item_type NOT NULL DEFAULT 'reading',
          topic TEXT,
          due_date DATE,
          estimated_minutes INTEGER CHECK (estimated_minutes IS NULL OR estimated_minutes >= 0),
          sort_order INTEGER NOT NULL DEFAULT 0,
          status study_plan_item_status NOT NULL DEFAULT 'todo',
          completed_at TIMESTAMPTZ,
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );

        CREATE TABLE quiz_questions (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          quiz_id UUID NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
          question_order INTEGER NOT NULL CHECK (question_order >= 0),
          question_type question_type NOT NULL DEFAULT 'multiple_choice',
          question_text TEXT NOT NULL,
          options JSONB NOT NULL DEFAULT '[]'::jsonb,
          correct_answer JSONB NOT NULL,
          explanation TEXT,
          points NUMERIC(8,2) NOT NULL DEFAULT 1 CHECK (points >= 0),
          topic TEXT,
          difficulty TEXT NOT NULL DEFAULT 'medium',
          source_chunk_ids UUID[] NOT NULL DEFAULT '{}',
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          UNIQUE (quiz_id, question_order),
          CONSTRAINT quiz_questions_difficulty_check CHECK (difficulty IN ('easy', 'medium', 'hard', 'mixed'))
        );

        CREATE TABLE quiz_attempts (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          quiz_id UUID NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
          user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          status attempt_status NOT NULL DEFAULT 'in_progress',
          started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          submitted_at TIMESTAMPTZ,
          graded_at TIMESTAMPTZ,
          score NUMERIC(8,2) NOT NULL DEFAULT 0 CHECK (score >= 0),
          max_score NUMERIC(8,2) NOT NULL DEFAULT 0 CHECK (max_score >= 0),
          percentage NUMERIC(5,2) CHECK (percentage IS NULL OR percentage BETWEEN 0 AND 100),
          time_spent_seconds INTEGER CHECK (time_spent_seconds IS NULL OR time_spent_seconds >= 0),
          weak_topics TEXT[] NOT NULL DEFAULT '{}',
          ai_feedback TEXT,
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );

        CREATE TABLE quiz_answers (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          attempt_id UUID NOT NULL REFERENCES quiz_attempts(id) ON DELETE CASCADE,
          question_id UUID NOT NULL REFERENCES quiz_questions(id) ON DELETE CASCADE,
          user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          answer JSONB NOT NULL,
          is_correct BOOLEAN,
          score_awarded NUMERIC(8,2) NOT NULL DEFAULT 0 CHECK (score_awarded >= 0),
          feedback TEXT,
          answered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          UNIQUE (attempt_id, question_id)
        );

        CREATE TABLE learning_analytics (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          topic TEXT NOT NULL,
          activity_date DATE NOT NULL DEFAULT CURRENT_DATE,
          source_document_id UUID REFERENCES uploaded_documents(id) ON DELETE SET NULL,
          last_quiz_attempt_id UUID REFERENCES quiz_attempts(id) ON DELETE SET NULL,
          study_minutes INTEGER NOT NULL DEFAULT 0 CHECK (study_minutes >= 0),
          ai_questions_count INTEGER NOT NULL DEFAULT 0 CHECK (ai_questions_count >= 0),
          quiz_attempt_count INTEGER NOT NULL DEFAULT 0 CHECK (quiz_attempt_count >= 0),
          questions_answered INTEGER NOT NULL DEFAULT 0 CHECK (questions_answered >= 0),
          correct_answers INTEGER NOT NULL DEFAULT 0 CHECK (correct_answers >= 0),
          wrong_answers INTEGER NOT NULL DEFAULT 0 CHECK (wrong_answers >= 0),
          avg_quiz_score NUMERIC(5,2) CHECK (avg_quiz_score IS NULL OR avg_quiz_score BETWEEN 0 AND 100),
          mastery_score NUMERIC(5,2) CHECK (mastery_score IS NULL OR mastery_score BETWEEN 0 AND 100),
          weakness_score NUMERIC(5,2) CHECK (weakness_score IS NULL OR weakness_score BETWEEN 0 AND 100),
          is_weak_topic BOOLEAN NOT NULL DEFAULT false,
          recommended_action TEXT,
          computed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          UNIQUE (user_id, topic, activity_date)
        );

        CREATE TABLE saved_notes (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
          title TEXT NOT NULL,
          content TEXT NOT NULL,
          source_type note_source_type NOT NULL DEFAULT 'manual',
          source_chat_message_id UUID REFERENCES ai_chat_messages(id) ON DELETE SET NULL,
          source_document_id UUID REFERENCES uploaded_documents(id) ON DELETE SET NULL,
          source_chunk_id UUID REFERENCES document_chunks(id) ON DELETE SET NULL,
          source_quiz_id UUID REFERENCES quizzes(id) ON DELETE SET NULL,
          source_quiz_attempt_id UUID REFERENCES quiz_attempts(id) ON DELETE SET NULL,
          tags TEXT[] NOT NULL DEFAULT '{}',
          is_pinned BOOLEAN NOT NULL DEFAULT false,
          metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
          created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );

        CREATE UNIQUE INDEX users_email_lower_uidx ON users (lower(email));

        CREATE INDEX uploaded_documents_user_status_idx ON uploaded_documents (user_id, status);
        CREATE INDEX uploaded_documents_user_created_idx ON uploaded_documents (user_id, created_at DESC);

        CREATE INDEX document_chunks_document_idx ON document_chunks (document_id, chunk_index);
        CREATE INDEX document_chunks_user_idx ON document_chunks (user_id);
        CREATE INDEX document_chunks_content_tsv_idx ON document_chunks USING GIN (to_tsvector('simple', content));
        CREATE INDEX document_chunks_metadata_gin_idx ON document_chunks USING GIN (metadata);
        CREATE UNIQUE INDEX document_chunks_vector_ref_uidx
          ON document_chunks (vector_store, vector_collection, vector_id)
          WHERE vector_id IS NOT NULL;

        CREATE INDEX ai_chat_sessions_user_idx ON ai_chat_sessions (user_id, last_message_at DESC);
        CREATE INDEX ai_chat_sessions_document_idx ON ai_chat_sessions (document_id);

        CREATE INDEX ai_chat_messages_session_idx ON ai_chat_messages (session_id, sequence_number);
        CREATE INDEX ai_chat_messages_user_created_idx ON ai_chat_messages (user_id, created_at DESC);
        CREATE INDEX ai_chat_messages_citations_gin_idx ON ai_chat_messages USING GIN (citations);

        CREATE INDEX study_plans_user_status_idx ON study_plans (user_id, status);
        CREATE INDEX study_plan_items_plan_status_idx ON study_plan_items (study_plan_id, status);
        CREATE INDEX study_plan_items_user_due_idx ON study_plan_items (user_id, due_date);

        CREATE INDEX quizzes_user_idx ON quizzes (user_id, created_at DESC);
        CREATE INDEX quizzes_source_document_idx ON quizzes (source_document_id);
        CREATE INDEX quizzes_topic_idx ON quizzes (topic);

        CREATE INDEX quiz_questions_quiz_order_idx ON quiz_questions (quiz_id, question_order);
        CREATE INDEX quiz_questions_topic_idx ON quiz_questions (topic);

        CREATE INDEX quiz_attempts_user_idx ON quiz_attempts (user_id, created_at DESC);
        CREATE INDEX quiz_attempts_quiz_user_idx ON quiz_attempts (quiz_id, user_id);
        CREATE INDEX quiz_attempts_weak_topics_gin_idx ON quiz_attempts USING GIN (weak_topics);

        CREATE INDEX quiz_answers_attempt_idx ON quiz_answers (attempt_id);
        CREATE INDEX quiz_answers_question_idx ON quiz_answers (question_id);

        CREATE INDEX learning_analytics_user_date_idx ON learning_analytics (user_id, activity_date DESC);
        CREATE INDEX learning_analytics_user_weak_idx ON learning_analytics (user_id, is_weak_topic, weakness_score DESC);
        CREATE INDEX learning_analytics_topic_idx ON learning_analytics (topic);

        CREATE INDEX saved_notes_user_created_idx ON saved_notes (user_id, created_at DESC);
        CREATE INDEX saved_notes_tags_gin_idx ON saved_notes USING GIN (tags);
        CREATE INDEX saved_notes_content_tsv_idx ON saved_notes USING GIN (to_tsvector('simple', title || ' ' || content));

        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
          NEW.updated_at = now();
          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER users_set_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER uploaded_documents_set_updated_at BEFORE UPDATE ON uploaded_documents FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER document_chunks_set_updated_at BEFORE UPDATE ON document_chunks FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER ai_chat_sessions_set_updated_at BEFORE UPDATE ON ai_chat_sessions FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER ai_chat_messages_set_updated_at BEFORE UPDATE ON ai_chat_messages FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER study_plans_set_updated_at BEFORE UPDATE ON study_plans FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER study_plan_items_set_updated_at BEFORE UPDATE ON study_plan_items FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER quizzes_set_updated_at BEFORE UPDATE ON quizzes FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER quiz_questions_set_updated_at BEFORE UPDATE ON quiz_questions FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER quiz_attempts_set_updated_at BEFORE UPDATE ON quiz_attempts FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER quiz_answers_set_updated_at BEFORE UPDATE ON quiz_answers FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER learning_analytics_set_updated_at BEFORE UPDATE ON learning_analytics FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER saved_notes_set_updated_at BEFORE UPDATE ON saved_notes FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TRIGGER IF EXISTS saved_notes_set_updated_at ON saved_notes;
        DROP TRIGGER IF EXISTS learning_analytics_set_updated_at ON learning_analytics;
        DROP TRIGGER IF EXISTS quiz_answers_set_updated_at ON quiz_answers;
        DROP TRIGGER IF EXISTS quiz_attempts_set_updated_at ON quiz_attempts;
        DROP TRIGGER IF EXISTS quiz_questions_set_updated_at ON quiz_questions;
        DROP TRIGGER IF EXISTS quizzes_set_updated_at ON quizzes;
        DROP TRIGGER IF EXISTS study_plan_items_set_updated_at ON study_plan_items;
        DROP TRIGGER IF EXISTS study_plans_set_updated_at ON study_plans;
        DROP TRIGGER IF EXISTS ai_chat_messages_set_updated_at ON ai_chat_messages;
        DROP TRIGGER IF EXISTS ai_chat_sessions_set_updated_at ON ai_chat_sessions;
        DROP TRIGGER IF EXISTS document_chunks_set_updated_at ON document_chunks;
        DROP TRIGGER IF EXISTS uploaded_documents_set_updated_at ON uploaded_documents;
        DROP TRIGGER IF EXISTS users_set_updated_at ON users;
        DROP FUNCTION IF EXISTS set_updated_at();

        DROP TABLE IF EXISTS saved_notes CASCADE;
        DROP TABLE IF EXISTS learning_analytics CASCADE;
        DROP TABLE IF EXISTS quiz_answers CASCADE;
        DROP TABLE IF EXISTS quiz_attempts CASCADE;
        DROP TABLE IF EXISTS quiz_questions CASCADE;
        DROP TABLE IF EXISTS study_plan_items CASCADE;
        DROP TABLE IF EXISTS quizzes CASCADE;
        DROP TABLE IF EXISTS study_plans CASCADE;
        DROP TABLE IF EXISTS ai_chat_messages CASCADE;
        DROP TABLE IF EXISTS ai_chat_sessions CASCADE;
        DROP TABLE IF EXISTS document_chunks CASCADE;
        DROP TABLE IF EXISTS uploaded_documents CASCADE;
        DROP TABLE IF EXISTS users CASCADE;

        DROP TYPE IF EXISTS note_source_type;
        DROP TYPE IF EXISTS attempt_status;
        DROP TYPE IF EXISTS question_type;
        DROP TYPE IF EXISTS quiz_status;
        DROP TYPE IF EXISTS quiz_source_type;
        DROP TYPE IF EXISTS study_plan_item_status;
        DROP TYPE IF EXISTS study_plan_item_type;
        DROP TYPE IF EXISTS study_plan_status;
        DROP TYPE IF EXISTS chat_role;
        DROP TYPE IF EXISTS chat_session_type;
        DROP TYPE IF EXISTS document_status;
        """
    )
