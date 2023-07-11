# polygon_pdf_gen
Generate &amp; Build Statement from Codeforces Polygon Packages

> This script provided a simple way to build statements from codeforces polygon packages.
>
> Noted that this script will **only server the Jiangxi Normal University ICPC school team for daily training**.

## Usage

1. First download the convert script `psbuild.py` to the target directory where you want to build the statements.

   ```
   git clone https://github.com/Heartfirey/polygon_pdf_gen.git /path/to/build/directory
   ```

2. Ensure you have pdflatex environment(if you have, then you can skip).

   - For Windows platform, we recommend you to install MikTex directory.

     - MikTex: [Home (miktex.org)](https://miktex.org/)
     - Or you can use Texlive: [TeX Live - TeX Users Group (tug.org)](https://tug.org/texlive/)

     After installation, you must ensure the command `pdflatex` could be excuted normally.

   - For linux platform, we also recommend you install MikTex(-w-#)

     - MikTex Installation Guidance: [Install MiKTeX for Linux](https://miktex.org/howto/install-miktex-unx)

3. Run this script:

   ```
   python psbuild.py [package directory] --output=[output_directory(with filename)] --problem_index=[problem index] --contest_name=[contest name] --contest_location=[contest location] --contest_date=[contest date] --statement_lang=[statement lang]
   ```

   - `[package directory]`: path to polygon package, for example `./problema`.
   - `[output_directory(with filename)]`: path to statements output directory. for example `./problemA.pdf`.
   - `[problem index]`: The index of problem in contest. it can be empty. For example `A`.
   - `[contest name]`: The name of your contest, it can be empty. For example `JXNU ACSNB Contest`.
   - `[contest_location]`: The location where you hold this contest, it can be empty. For example `Nanchang, Jiangxi`.
   - `[contest_date]`: The contest date, it can be empty. For example `2023-07-12.`
   - `[statemetn_lang]`: Default set to `english`, this option should be same as the lang option in polyon.

