"""Generate the detailed guide and formula from their canonical sources."""
import subprocess
import sys
from definition_lib import ROOT, implementation_text


def main():
    target = ROOT / '전문가 에이전트 정의 2.md'
    target.write_text(implementation_text())
    subprocess.run([sys.executable, str(ROOT / 'docs/전개-수식/전개-수식-gen.py')],
                   check=True, cwd=ROOT)
    print('정의 2·구성 도식 생성 완료')


if __name__ == '__main__':
    main()
