import pytest
import os
import subprocess
import sys
import filecmp
# Tento soubor je v češtině pro srozumitelnost výstupních debug zpráv
class TestSelfReplicator:
    """Testovací třída pro samoreplikující se skript."""
    
    @pytest.fixture(autouse=True)
    def setup_and_cleanup(self):
        """Příprava před testem a úklid po testu."""

        self.main_file = "main.py"
        self.gen1_file = self.main_file + "new.py"
        self.gen2_file = self.gen1_file + "new.py"
        
        self.cleanup_generated_files()
        
        yield
        
        self.cleanup_generated_files()
    
    def cleanup_generated_files(self):
        """Odstranění vygenerovaných souborů."""
        for file in [self.gen1_file, self.gen2_file]:
            if os.path.exists(file):
                os.remove(file)
                
    def test_file_creation(self):
        """Test, zda skript vytvoří nový soubor."""
        result = subprocess.run([sys.executable, self.main_file], 
                               capture_output=True, text=True)
        
        assert result.returncode == 0, f"Skript selhal s chybou: {result.stderr}"
        
        assert os.path.exists(self.gen1_file), \
               f"Soubor {self.gen1_file} nebyl vytvořen!"
    
    def test_file_content(self):
        """Test, zda obsah nového souboru odpovídá původnímu."""
        subprocess.run([sys.executable, self.main_file], capture_output=True)
        
        with open(self.main_file, 'r', encoding='utf-8') as f:
            original = f.read()
        
        with open(self.gen1_file, 'r', encoding='utf-8') as f:
            generated = f.read()
        
        assert original.strip() == generated.strip(), \
               "Obsah vygenerovaného souboru se liší od originálu!"
    
    def test_recursive_generation(self):
        """Test, zda vygenerovaný soubor je také funkční a může generovat další kopii."""
        subprocess.run([sys.executable, self.main_file], capture_output=True)
        
        result = subprocess.run([sys.executable, self.gen1_file], 
                               capture_output=True, text=True)
        
        assert result.returncode == 0, \
               f"Vygenerovaný skript selhal s chybou: {result.stderr}"
        
        assert os.path.exists(self.gen2_file), \
               f"Soubor druhé generace {self.gen2_file} nebyl vytvořen!"
        
        assert filecmp.cmp(self.main_file, self.gen1_file, shallow=False), \
               "Obsah souboru první generace se liší od originálu!"
        assert filecmp.cmp(self.gen1_file, self.gen2_file, shallow=False), \
               "Obsah souboru druhé generace se liší od první generace!"
    
    def test_console_output(self):
        """Test, zda výpis na konzoli odpovídá obsahu souboru."""
        result = subprocess.run([sys.executable, self.main_file], 
                               capture_output=True, text=True)
        
        with open(self.gen1_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        assert result.stdout.strip() == file_content.strip(), \
               "Výstup na konzoli neodpovídá obsahu vygenerovaného souboru!"
    
    def test_unicode_escape_handling(self):
        """Test správné práce s Unicode escapy v self-reference."""
        subprocess.run([sys.executable, self.main_file], capture_output=True)
        
        subprocess.run([sys.executable, self.gen1_file], capture_output=True)
        
        with open(self.gen2_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert r"\042" in content, "Vygenerovaný kód neobsahuje správné Unicode escapy!"
        
        assert "print_statements = [r" in content, \
               "Vygenerovaný kód neobsahuje správnou inicializaci seznamu print_statements!"

if __name__ == "__main__":
    pytest.main(["-v", __file__])