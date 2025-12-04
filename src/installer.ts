import { fileURLToPath } from "url";
import { dirname, join, resolve } from "path";
import {
  existsSync,
  mkdirSync,
  copyFileSync,
  readdirSync,
  statSync,
} from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const TEMPLATES_DIR = join(__dirname, "..", "templates");

export interface InstallOptions {
  force?: boolean;
  dryRun?: boolean;
}

export interface InstallResult {
  success: boolean;
  copied: string[];
  skipped: string[];
  error?: string;
}

function copyFilesRecursively(
  srcDir: string,
  destDir: string,
  force: boolean
): { copied: string[]; skipped: string[] } {
  const copied: string[] = [];
  const skipped: string[] = [];

  function processDir(src: string, dest: string, relativePath = "") {
    if (!existsSync(dest)) {
      mkdirSync(dest, { recursive: true });
    }

    const entries = readdirSync(src);

    for (const entry of entries) {
      const srcPath = join(src, entry);
      const destPath = join(dest, entry);
      const relPath = relativePath ? join(relativePath, entry) : entry;

      if (statSync(srcPath).isDirectory()) {
        processDir(srcPath, destPath, relPath);
      } else {
        if (existsSync(destPath) && !force) {
          skipped.push(relPath);
        } else {
          const parentDir = dirname(destPath);
          if (!existsSync(parentDir)) {
            mkdirSync(parentDir, { recursive: true });
          }
          copyFileSync(srcPath, destPath);
          copied.push(relPath);
        }
      }
    }
  }

  processDir(srcDir, destDir);
  return { copied, skipped };
}

/**
 * Install spec2impl templates to a target directory
 * Merges with existing .claude directory without overwriting (unless force is true)
 */
export function install(
  targetDir: string,
  options: InstallOptions = {}
): InstallResult {
  const projectRoot = resolve(targetDir);
  const claudeDir = join(projectRoot, ".claude");
  const templateClaudeDir = join(TEMPLATES_DIR, ".claude");

  if (!existsSync(TEMPLATES_DIR)) {
    return {
      success: false,
      copied: [],
      skipped: [],
      error: "Template directory not found. Package may be corrupted.",
    };
  }

  if (options.dryRun) {
    // Dry run: just list files that would be copied
    const { copied, skipped } = copyFilesRecursively(
      templateClaudeDir,
      claudeDir,
      options.force || false
    );
    return {
      success: true,
      copied: copied.map((f) => `.claude/${f}`),
      skipped: skipped.map((f) => `.claude/${f}`),
    };
  }

  try {
    const { copied, skipped } = copyFilesRecursively(
      templateClaudeDir,
      claudeDir,
      options.force || false
    );
    return {
      success: true,
      copied: copied.map((f) => `.claude/${f}`),
      skipped: skipped.map((f) => `.claude/${f}`),
    };
  } catch (error) {
    return {
      success: false,
      copied: [],
      skipped: [],
      error: error instanceof Error ? error.message : String(error),
    };
  }
}
