import { fileURLToPath } from "url";
import { dirname, join, resolve } from "path";
import { existsSync, cpSync, readdirSync, statSync } from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const TEMPLATES_DIR = join(__dirname, "..", "templates");

export interface InstallOptions {
  force?: boolean;
  dryRun?: boolean;
}

export interface InstallResult {
  success: boolean;
  files: string[];
  error?: string;
}

function getFilesToCopy(dir: string, base = ""): string[] {
  const files: string[] = [];
  const entries = readdirSync(dir);

  for (const entry of entries) {
    const fullPath = join(dir, entry);
    const relativePath = base ? join(base, entry) : entry;

    if (statSync(fullPath).isDirectory()) {
      files.push(...getFilesToCopy(fullPath, relativePath));
    } else {
      files.push(relativePath);
    }
  }

  return files;
}

/**
 * Install spec2impl templates to a target directory
 */
export function install(
  targetDir: string,
  options: InstallOptions = {}
): InstallResult {
  const projectRoot = resolve(targetDir);
  const claudeDir = join(projectRoot, ".claude");

  if (!existsSync(TEMPLATES_DIR)) {
    return {
      success: false,
      files: [],
      error: "Template directory not found. Package may be corrupted.",
    };
  }

  if (existsSync(claudeDir) && !options.force) {
    return {
      success: false,
      files: [],
      error: ".claude directory already exists. Use force option to overwrite.",
    };
  }

  const files = getFilesToCopy(join(TEMPLATES_DIR, ".claude")).map(
    (f) => `.claude/${f}`
  );

  if (options.dryRun) {
    return {
      success: true,
      files,
    };
  }

  try {
    cpSync(join(TEMPLATES_DIR, ".claude"), claudeDir, { recursive: true });
    return {
      success: true,
      files,
    };
  } catch (error) {
    return {
      success: false,
      files: [],
      error: error instanceof Error ? error.message : String(error),
    };
  }
}
