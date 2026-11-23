// main.ts — entry program for the make.fun bounty "Post a GTA 6 meme on X".
//
// The entry itself is the X post: its address lives in POST.json at the
// repository root. This program carries that file into the grader's
// output directory, unchanged. It reads POST.json, checks that it parses
// as JSON holding a `url` string, then writes the very same bytes out.
//
// Standard library only. No network. Deterministic: the same input
// always produces the same output bytes. Any failure (missing file,
// bad JSON, no url, unwritable output) prints an error and exits
// non-zero, so a bad entry fails loudly instead of silently.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const FILE_NAME = "POST.json";

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

function main(): void {
  const sourcePath = join(botDir, FILE_NAME);
  const destPath = join(outputDir, FILE_NAME);

  if (!existsSync(sourcePath)) {
    fail(`cannot find ${sourcePath}`);
  }

  let text: string;
  try {
    text = readFileSync(sourcePath, "utf8");
  } catch (err) {
    fail(`cannot read ${sourcePath}: ${(err as Error).message}`);
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(text);
  } catch (err) {
    fail(`${sourcePath} is not valid JSON: ${(err as Error).message}`);
  }

  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
    fail(`${sourcePath} must hold a JSON object, not an array or a bare value`);
  }

  const url = (parsed as Record<string, unknown>).url;
  if (typeof url !== "string" || url.trim().length === 0) {
    fail(`${sourcePath} must hold a "url" string naming the X post`);
  }
  if (!/^https?:\/\//.test(url)) {
    fail(`"url" in ${sourcePath} must start with http:// or https://, got ${url}`);
  }
  if (url.includes("<") || url.includes(">")) {
    // Not fatal: the placeholder URL is expected before the post is live,
    // but warn loudly so a placeholder is never submitted by mistake.
    console.error(`main.ts: warning: "url" in ${sourcePath} still looks like a placeholder: ${url}`);
  }

  try {
    mkdirSync(outputDir, { recursive: true });
  } catch (err) {
    fail(`cannot create output directory ${outputDir}: ${(err as Error).message}`);
  }

  try {
    writeFileSync(destPath, text, "utf8");
  } catch (err) {
    fail(`cannot write ${destPath}: ${(err as Error).message}`);
  }

  // Prove the copy landed intact: read it back and compare bytes.
  let written: string;
  try {
    written = readFileSync(destPath, "utf8");
  } catch (err) {
    fail(`cannot read back ${destPath}: ${(err as Error).message}`);
  }
  if (written !== text) {
    fail(`${destPath} differs from ${sourcePath} after writing`);
  }

  console.log(`wrote ${destPath}`);
}

main();
