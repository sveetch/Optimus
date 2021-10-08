from webassets import Bundle

from optimus.assets.registry import AssetRegistry


def test_empty():
    registry = AssetRegistry()

    assert registry.map_dest_to_bundle == {}


def test_add_bundle():
    registry = AssetRegistry()

    # Dummy bundles
    bundle_modernizr = Bundle(
        "js/modernizr.src.js", filters=None, output="js/modernizr.min.js"
    )

    bundle_css = Bundle(
        "css/app.css", "css/dummy.css", filters=None, output="css/app.min.css"
    )

    # Registering
    registry.add_bundle("modernizr_js", bundle_modernizr)
    registry.add_bundle("app_css", bundle_css)

    assert len(registry.map_dest_to_bundle.keys()) == 3
    assert registry.map_dest_to_bundle["css/app.css"] == "app_css"
    assert registry.map_dest_to_bundle["css/dummy.css"] == "app_css"
    assert registry.map_dest_to_bundle["js/modernizr.src.js"] == "modernizr_js"
