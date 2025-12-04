#!/usr/bin/env node

import { program } from "commander";
import chalk from "chalk";
import ora from "ora";
import { fileURLToPath } from "url";
import { dirname, join, resolve } from "path";
import { existsSync, mkdirSync, cpSync, readdirSync, statSync } from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// テンプレートディレクトリのパス（パッケージルートからの相対パス）
const TEMPLATES_DIR = join(__dirname, "..", "templates");

interface InstallOptions {
  force?: boolean;
  dryRun?: boolean;
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

function install(targetDir: string, options: InstallOptions = {}) {
  const spinner = ora("Installing spec2impl...").start();

  const projectRoot = resolve(targetDir);
  const claudeDir = join(projectRoot, ".claude");

  // テンプレートディレクトリの存在確認
  if (!existsSync(TEMPLATES_DIR)) {
    spinner.fail(chalk.red("Template directory not found. Package may be corrupted."));
    process.exit(1);
  }

  // 既存の .claude ディレクトリの確認
  if (existsSync(claudeDir) && !options.force) {
    spinner.warn(chalk.yellow(".claude directory already exists."));
    console.log("");
    console.log(chalk.cyan("Options:"));
    console.log("  --force    Overwrite existing files");
    console.log("");
    console.log(chalk.dim("Run with --force to overwrite existing configuration."));
    process.exit(1);
  }

  // ドライランモード
  if (options.dryRun) {
    spinner.info(chalk.cyan("Dry run mode - no files will be created"));
    console.log("");
    console.log(chalk.bold("Files to be installed:"));

    const files = getFilesToCopy(join(TEMPLATES_DIR, ".claude"));
    for (const file of files) {
      console.log(chalk.dim(`  .claude/${file}`));
    }
    return;
  }

  try {
    // .claude ディレクトリをコピー
    cpSync(join(TEMPLATES_DIR, ".claude"), claudeDir, { recursive: true });

    spinner.succeed(chalk.green("spec2impl installed successfully!"));

    console.log("");
    console.log(chalk.bold("Installed files:"));
    console.log(chalk.dim("  .claude/commands/spec2impl.md"));
    console.log(chalk.dim("  .claude/agents/spec2impl/"));
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
