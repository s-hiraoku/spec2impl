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

interface InstallOptions {
  force?: boolean;
  dryRun?: boolean;
}

interface FileInfo {
  relativePath: string;
  exists: boolean;
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
      files.push(...getFilesToCopy(templateDir, targetDir, relativePath));
    } else {
      files.push({
        relativePath,
        exists: existsSync(targetPath),
      });
    }
  }

  return files;
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
          // 親ディレクトリを作成
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
      if (file.exists && !options.force) {
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
    // ファイル単位でコピー（既存ファイルはスキップ or 上書き）
    const { copied, skipped } = copyFilesRecursively(
      templateClaudeDir,
      claudeDir,
      options.force || false
    );

    spinner.succeed(chalk.green("spec2impl installed successfully!"));

    console.log("");
    if (copied.length > 0) {
      console.log(chalk.bold("Installed files:"));
      for (const file of copied) {
        console.log(chalk.dim(`  .claude/${file}`));
      }
    }

    if (skipped.length > 0) {
      console.log("");
      console.log(chalk.yellow("Skipped (already exist):"));
      for (const file of skipped) {
        console.log(chalk.dim(`  .claude/${file}`));
      }
      console.log(chalk.dim("\n  Use --force to overwrite existing files."));
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
  .version("0.1.0");

program
  .command("init")
  .description("Install spec2impl slash command and agents to current project")
  .argument("[directory]", "Target project directory", ".")
  .option("-f, --force", "Overwrite existing .claude directory")
  .option("--dry-run", "Preview files without installing")
  .action((directory: string, options: InstallOptions) => {
    install(directory, options);
  });

// デフォルトコマンド（引数なしで実行した場合）
program
  .argument("[directory]", "Target project directory (defaults to current directory)")
  .option("-f, --force", "Overwrite existing .claude directory")
  .option("--dry-run", "Preview files without installing")
  .action((directory: string | undefined, options: InstallOptions) => {
    if (directory && !directory.startsWith("-")) {
      install(directory, options);
    } else {
      install(".", options);
    }
  });

program.parse();
