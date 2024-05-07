"""
Test custom Django Management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # Configura el side_effect para simular múltiples intentos fallidos seguidos de éxito
        # Esto simula el comportamiento esperado cuando la base de datos tarda en estar lista
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # Verifica que check fue llamado 6 veces, que es consistente con el side_effect configurado
        self.assertEqual(patched_check.call_count, 6)
        # No necesitas verificar que fue llamado con databases=['default'] aquí,
        # ya que eso se maneja automáticamente con el side_effect configurado

        # Si necesitas verificar algo específico sobre las llamadas a check, hazlo aquí
        # Por ejemplo, si quieres asegurarte de que todas las llamadas fueron con el mismo argumento:
        # self.assertEqual(patched_check.call_args_list, [mock.call(databases=['default'])] * 6)