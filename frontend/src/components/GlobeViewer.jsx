import React, { useEffect, useRef } from 'react';
import * as Cesium from 'cesium';

export default function GlobeViewer({ orbitData }) {
    const cesiumContainer = useRef(null);
    const viewerRef = useRef(null);

    useEffect(() => {
        if (!viewerRef.current && cesiumContainer.current) {
            viewerRef.current = new Cesium.Viewer(cesiumContainer.current, {
                animation: false,
                timeline: false,
                scene3DOnly: true,
                baseLayerPicker: false,
                geocoder: false,
                homeButton: false,
                navigationHelpButton: false,
                sceneModePicker: false,
                fullscreenButton: false,
                infoBox: false,
                selectionIndicator: false,
                requestRenderMode: true,
                maximumRenderTimeChange: Infinity,
                terrainProvider: new Cesium.EllipsoidTerrainProvider(),
            });

            const viewer = viewerRef.current;

            viewer.scene.globe.enableLighting = false;
            viewer.scene.skyAtmosphere.show = false;
            viewer.shadows = false;
            viewer.resolutionScale = 0.7;
        }

        const viewer = viewerRef.current;
        viewer.entities.removeAll();

        if (orbitData && orbitData.path1 && orbitData.path2) {
            viewer.entities.add({
                name: 'Orbit 1',
                polyline: {
                    positions: Cesium.Cartesian3.fromDegreesArrayHeights(orbitData.path1),
                    width: 3,
                    material: new Cesium.PolylineGlowMaterialProperty({
                        glowPower: 0.2,
                        taperPower: 0.5,
                        color: Cesium.Color.fromCssColorString('#00d2ff'),
                    }),
                },
            });

            viewer.entities.add({
                name: 'Orbit 2',
                polyline: {
                    positions: Cesium.Cartesian3.fromDegreesArrayHeights(orbitData.path2),
                    width: 3,
                    material: new Cesium.PolylineGlowMaterialProperty({
                        glowPower: 0.2,
                        taperPower: 0.5,
                        color: Cesium.Color.fromCssColorString('#facc15'),
                    }),
                },
            });

            if (orbitData.closest_point) {
                viewer.entities.add({
                    name: 'Closest Approach',
                    position: Cesium.Cartesian3.fromDegrees(
                        orbitData.closest_point[0],
                        orbitData.closest_point[1],
                        orbitData.closest_point[2]
                    ),
                    point: {
                        pixelSize: 15,
                        color: Cesium.Color.RED,
                        outlineColor: Cesium.Color.WHITE,
                        outlineWidth: 2,
                    }
                });
            }

            viewer.zoomTo(viewer.entities);
            viewer.scene.requestRender();
        }

        return () => { };
    }, [orbitData]);

    return <div ref={cesiumContainer} className="globe-container" />;
}
