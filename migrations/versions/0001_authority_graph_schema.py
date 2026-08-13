"""patala-atlas: initial Authority Graph schema

Revision ID: 0001
Revises: None
Create Date: 2026-08-13

Implements the Pāṭala Authority Graph SQL schema from
docs/vision/atlas/technical-architecture-v1.md (§17–26, §44–46):
  work, person, institution, edition, witness, surrogate, transcription, etext, source,
  scholarly_work, external_identifier, name_variant, relationship,
  asset, asset_version, rights, authority_evidence,
  passage, passage_version, scholarly_object, scholarly_object_version, object_dependency.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── core entities ─────────────────────────────────────────────────────
    op.create_table(
        "work",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("canonical_title", sa.Text(), nullable=False),
        sa.Column("title_normalized", sa.Text(), nullable=False),
        sa.Column("work_type", sa.Text(), nullable=False),
        sa.Column("language", sa.ARRAY(sa.Text()), nullable=True),
        sa.Column("tradition", sa.ARRAY(sa.Text()), nullable=True),
        sa.Column("date_min", sa.Integer(), nullable=True),
        sa.Column("date_max", sa.Integer(), nullable=True),
        sa.Column("date_note", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "person",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("canonical_name", sa.Text(), nullable=False),
        sa.Column("name_normalized", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "institution",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("canonical_name", sa.Text(), nullable=False),
        sa.Column("name_normalized", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "edition",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("work_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("work.id"), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("edition_type", sa.Text(), nullable=False),
        sa.Column("publication_year", sa.Integer(), nullable=True),
        sa.Column("publisher", sa.Text(), nullable=True),
        sa.Column("series", sa.Text(), nullable=True),
        sa.Column("volume", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("authority_state", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "witness",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("work_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("work.id"), nullable=True),
        sa.Column("institution_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("institution.id"), nullable=True),
        sa.Column("shelfmark", sa.Text(), nullable=True),
        sa.Column("material", sa.Text(), nullable=True),
        sa.Column("script", sa.Text(), nullable=True),
        sa.Column("language", sa.ARRAY(sa.Text()), nullable=True),
        sa.Column("date_min", sa.Integer(), nullable=True),
        sa.Column("date_max", sa.Integer(), nullable=True),
        sa.Column("folio_count", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("authority_state", sa.Text(), nullable=False),
    )
    op.create_table(
        "surrogate",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("witness_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("witness.id"), nullable=False),
        sa.Column("surrogate_type", sa.Text(), nullable=False),
        sa.Column("iiif_manifest", sa.Text(), nullable=True),
        sa.Column("external_url", sa.Text(), nullable=True),
        sa.Column("rights_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("authority_state", sa.Text(), nullable=False),
    )
    op.create_table(
        "etext",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("work_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("work.id"), nullable=False),
        sa.Column("edition_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("edition.id"), nullable=True),
        sa.Column("provider", sa.Text(), nullable=True),
        sa.Column("provider_record", sa.Text(), nullable=True),
        sa.Column("transcription_method", sa.Text(), nullable=True),
        sa.Column("authority_state", sa.Text(), nullable=False),
        sa.Column("current_asset_version", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_table(
        "scholarly_work",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("work_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("work.id"), nullable=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("authority_state", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "source",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("work_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("work.id"), nullable=False),
        sa.Column("etext_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("etext.id"), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("payload_hash", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # ── rights / assets ───────────────────────────────────────────────────
    op.create_table(
        "rights",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("rights_status", sa.Text(), nullable=False),
        sa.Column("license", sa.Text(), nullable=True),
        sa.Column("rights_holder", sa.Text(), nullable=True),
        sa.Column("hosting_allowed", sa.Boolean(), nullable=True),
        sa.Column("redistribution_allowed", sa.Boolean(), nullable=True),
        sa.Column("machine_processing_allowed", sa.Boolean(), nullable=True),
        sa.Column("derivative_allowed", sa.Boolean(), nullable=True),
        sa.Column("evidence_ref", sa.Text(), nullable=True),
    )
    op.create_table(
        "asset",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("entity_type", sa.Text(), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),
    )
    op.create_table(
        "asset_version",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("asset.id"), nullable=False),
        sa.Column("sha256", sa.LargeBinary(), nullable=False, unique=True),
        sa.Column("media_type", sa.Text(), nullable=False),
        sa.Column("byte_size", sa.BigInteger(), nullable=False),
        sa.Column("r2_bucket", sa.Text(), nullable=True),
        sa.Column("r2_key", sa.Text(), nullable=True),
        sa.Column("external_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # ── identifiers / names / relationships / authority evidence ──────────
    op.create_table(
        "external_identifier",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("entity_type", sa.Text(), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("scheme", sa.Text(), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("raw_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.UniqueConstraint("scheme", "value", name="uq_external_identifier_scheme_value"),
    )
    op.create_table(
        "name_variant",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("entity_type", sa.Text(), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("variant", sa.Text(), nullable=False),
        sa.Column("normalized", sa.Text(), nullable=False),
    )
    op.create_table(
        "relationship",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_type", sa.Text(), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("relation", sa.Text(), nullable=False),
        sa.Column("target_type", sa.Text(), nullable=False),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("evidence", sa.Text(), nullable=True),
    )
    op.create_table(
        "authority_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("subject_type", sa.Text(), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dimension", sa.Text(), nullable=False),
        sa.Column("source_scheme", sa.Text(), nullable=False),
        sa.Column("source_record", sa.Text(), nullable=True),
        sa.Column("relation", sa.Text(), nullable=False),
        sa.Column("evidence_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("asserted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reviewer_ref", postgresql.UUID(as_uuid=True), nullable=True),
    )

    # ── passages / scholarly objects / dependencies ───────────────────────
    op.create_table(
        "passage",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("work_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("work.id"), nullable=False),
        sa.Column("parent_passage_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("passage.id"), nullable=True),
        sa.Column("ordinal", sa.Integer(), nullable=True),
        sa.Column("canonical_locator", sa.Text(), nullable=False),
    )
    op.create_table(
        "passage_version",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("passage_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("passage.id"), nullable=False),
        sa.Column("source_version_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("text_original", sa.Text(), nullable=False),
        sa.Column("text_normalized", sa.Text(), nullable=True),
        sa.Column("content_hash", sa.Text(), nullable=False),
        sa.Column("schema_version", sa.Text(), nullable=False),
    )
    op.create_table(
        "scholarly_object",
        sa.Column("object_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("object_type", sa.Text(), nullable=False),
    )
    op.create_table(
        "scholarly_object_version",
        sa.Column("version_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("object_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scholarly_object.object_id"), nullable=False),
        sa.Column("schema_name", sa.Text(), nullable=False),
        sa.Column("schema_version", sa.Text(), nullable=False),
        sa.Column("payload_jsonb", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("payload_hash", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "object_dependency",
        sa.Column("consumer_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dependency_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("relation", sa.Text(), nullable=False),
        sa.Column("load_bearing", sa.Boolean(), nullable=True),
        sa.Column("epistemic_role", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("consumer_version_id", "dependency_version_id", "relation"),
    )

    # ── indexes for search (pg_trgm / unaccent are enabled separately) ────
    op.create_index("ix_work_title_normalized", "work", ["title_normalized"])
    op.create_index("ix_edition_work_id", "edition", ["work_id"])
    op.create_index("ix_witness_work_id", "witness", ["work_id"])
    op.create_index("ix_etext_work_id", "etext", ["work_id"])
    op.create_index("ix_asset_version_sha256", "asset_version", ["sha256"])


def downgrade() -> None:
    for t in ("object_dependency", "scholarly_object_version", "scholarly_object", "passage_version",
              "passage", "authority_evidence", "relationship", "name_variant", "external_identifier",
              "asset_version", "asset", "rights", "source", "scholarly_work", "etext", "surrogate",
              "witness", "edition", "institution", "person", "work"):
        op.drop_table(t)
