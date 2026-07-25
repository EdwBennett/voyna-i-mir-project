import argostranslate.package
import argostranslate.translate

from_code = "ru"
to_code = "en"

argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(lambda x: x.from_code == from_code and x.to_code == to_code, available_packages)
)

argostranslate.package.install_from_path(package_to_install.download())

print(argostranslate.translate.translate("Привет мир", from_code, to_code))
