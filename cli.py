# TODO DEV-PRIOR: CLI for optimization
# (see https://click.palletsprojects.com/en/8.1.x/)
""" reqs:
    - variant option
    - config path option
"""
import click
import os
from yaml import safe_load
from calculator import get_dto, get_optimizer


@click.command('optimize')
@click.option('--variant', '-v', required=True, type=int, help='Доступные варианты% 15, 16, 17, 18')
@click.option('--config', '-c', required=False, help='Путь до конфигурации (по умолчанию ./config.yml)')
def optimize(variant: int, config: str):
    config = config or 'config.yml'
    if variant not in (15, 16, 17, 18):
        raise click.exceptions.BadParameter(f'Некорректный вариант: {variant}')
    dto_cls = get_dto(variant)
    if not dto_cls:
        raise click.exceptions.UsageError(f'Не удалось получить DTO для варианта {variant}')
    optimizer_cls = get_optimizer(variant)
    if not optimizer_cls:
        raise click.exceptions.UsageError(f'Не удалось Оптимизатор для варианта {variant}')
    if not os.path.isfile(config):
        raise click.exceptions.FileError(f'Некорректный путь до конфигурации: {config}')
    try:
        data = safe_load(open(config))
    except Exception as err:
        raise click.exceptions.FileError(f'Ошибка чтения файла {config}:\n{str(err)}')
    dto = dto_cls(data)
    optimizer = optimizer_cls(dto)
    optimizer.calculate()


if __name__ == '__main__':
    import sys

    sys.tracebacklimit = 0
    optimize()
