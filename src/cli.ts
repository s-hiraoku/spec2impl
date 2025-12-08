#!/usr/bin/env node

import { program } from "commander";
import chalk from "chalk";
import ora from "ora";
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

// テンプレートディレクトリのパス（パッケージルートからの相対パス）
const TEMPLATES_DIR = join(__dirname, "..", "templates");

// spec2impl が管理するパス（常に上書き対象）
const SPEC2IMPL_PATHS = [
  "commands/spec2impl.md",
  "agents/spec2impl/",
  "skills/skill-creator/",
];

interface InstallOptions {
  force?: boolean;
  dryRun?: boolean;
}

interface FileInfo {
  relativePath: string;
  exists: boolean;
  isSpec2implManaged: boolean;
}

/**
 * ファイルが spec2impl 管理下かどうかを判定
 */
function isSpec2implManagedPath(relativePath: string): boolean {
  return SPEC2IMPL_PATHS.some(
    (managedPath) =>
      relativePath === managedPath ||
      relativePath.startsWith(managedPath)
  );
}

function getFilesToCopy(
  templateDir: string,
  targetDir: string,
  base = ""
): FileInfo[] {
  const files: FileInfo[] = [];
  const entries = readdirSync(templateDir);

  for (const entry of entries) {
    const templatePath = join(templateDir, entry);
    const relativePath = base ? join(base, entry) : entry;
    const targetPath = join(targetDir, relativePath);

    if (statSync(templatePath).isDirectory()) {
      files.push(...getFilesToCopy(templatePath, targetDir, relativePath));
    } else {
      files.push({
        relativePath,
        exists: existsSync(targetPath),
        isSpec2implManaged: isSpec2implManagedPath(relativePath),
      });
    }
  }

  return files;
}

function copyFilesRecursively(
  srcDir: string,
  destDir: string,
  force: boolean
): { copied: string[]; skipped: string[]; updated: string[] } {
  const copied: string[] = [];
  const skipped: string[] = [];
  const updated: string[] = [];

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
        const isManaged = isSpec2implManagedPath(relPath);
        const fileExists = existsSync(destPath);

        // spec2impl 管理ファイルは常に上書き、それ以外は force が必要
        if (fileExists && !isManaged && !force) {
          skipped.push(relPath);
        } else {
          // 親ディレクトリを作成
          const parentDir = dirname(destPath);
          if (!existsSync(parentDir)) {
            mkdirSync(parentDir, { recursive: true });
          }
          copyFileSync(srcPath, destPath);

          if (fileExists && isManaged) {
            updated.push(relPath);
          } else {
            copied.push(relPath);
          }
        }
      }
    }
  }

  processDir(srcDir, destDir);
  return { copied, skipped, updated };
}

function install(targetDir: string, options: InstallOptions = {}) {
  const spinner = ora("Installing spec2impl...").start();

  const projectRoot = resolve(targetDir);
  const claudeDir = join(projectRoot, ".claude");
  const templateClaudeDir = join(TEMPLATES_DIR, ".claude");

  // テンプレートディレクトリの存在確認
  if (!existsSync(TEMPLATES_DIR)) {
    spinner.fail(
      chalk.red("Template directory not found. Package may be corrupted.")
    );
    process.exit(1);
  }

  // ドライランモード
  if (options.dryRun) {
    spinner.info(chalk.cyan("Dry run mode - no files will be created"));
    console.log("");
    console.log(chalk.bold("Files to be installed:"));

    const files = getFilesToCopy(templateClaudeDir, claudeDir);
    for (const file of files) {
      if (file.exists && file.isSpec2implManaged) {
        console.log(chalk.cyan(`  .claude/${file.relativePath} (update)`));
      } else if (file.exists && !options.force) {
        console.log(chalk.yellow(`  .claude/${file.relativePath} (skip - exists)`));
      } else if (file.exists && options.force) {
        console.log(chalk.cyan(`  .claude/${file.relativePath} (overwrite)`));
      } else {
        console.log(chalk.green(`  .claude/${file.relativePath}`));
      }
    }
    return;
  }

  try {
    // ファイル単位でコピー
    const { copied, skipped, updated } = copyFilesRecursively(
      templateClaudeDir,
      claudeDir,
      options.force || false
    );

    spinner.succeed(chalk.green("spec2impl installed successfully!"));

    console.log("");

    if (updated.length > 0) {
      console.log(chalk.bold("Updated files:"));
      for (const file of updated) {
        console.log(chalk.cyan(`  .claude/${file}`));
      }
      console.log("");
    }

    if (copied.length > 0) {
      console.log(chalk.bold("Installed files:"));
      for (const file of copied) {
        console.log(chalk.dim(`  .claude/${file}`));
      }
    }

    if (skipped.length > 0) {
      console.log("");
      console.log(chalk.yellow("Skipped (user files):"));
      for (const file of skipped) {
        console.log(chalk.dim(`  .claude/${file}`));
      }
      console.log(chalk.dim("\n  Use --force to overwrite user files."));
    }

    console.log("");
    console.log(chalk.bold("Next steps:"));
    console.log("");
    console.log(chalk.cyan("  1. Open Claude Code in this project"));
    console.log(chalk.cyan("  2. Run the command:"));
    console.log("");
    console.log(chalk.bold.white("     /spec2impl docs/"));
    console.log("");
    console.log(chalk.dim("  Replace 'docs/' with your specification directory."));
    console.log("");
  } catch (error) {
    spinner.fail(chalk.red("Installation failed"));
    console.error(error);
    process.exit(1);
  }
}

program
  .name("spec2impl")
  .description("Generate Claude Code implementation environment from specification documents")
  .version("0.2.1");

program
  .command("init")
  .description("Install spec2impl slash command and agents to current project")
  .argument("[directory]", "Target project directory", ".")
  .option("-f, --force", "Overwrite all existing files (including user files)")
  .option("--dry-run", "Preview files without installing")
  .action((directory: string, options: InstallOptions) => {
    install(directory, options);
  });

// デフォルトコマンド（引数なしで実行した場合）
program
  .argument("[directory]", "Target project directory (defaults to current directory)")
  .option("-f, --force", "Overwrite all existing files (including user files)")
  .option("--dry-run", "Preview files without installing")
  .action((directory: string | undefined, options: InstallOptions) => {
    if (directory && !directory.startsWith("-")) {
      install(directory, options);
    } else {
      install(".", options);
    }
  });

program.parse();
