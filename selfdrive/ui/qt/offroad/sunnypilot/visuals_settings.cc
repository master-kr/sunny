#include "selfdrive/ui/qt/offroad/sunnypilot/visuals_settings.h"

VisualsPanel::VisualsPanel(QWidget *parent) : ListWidget(parent) {
  // param, title, desc, icon
  std::vector<std::tuple<QString, QString, QString, QString>> toggle_defs{
    {
      "BrakeLights",
      tr("Display Braking Status"),
      tr("Enable this will turn the current speed value to red while the brake is used."),
      "../assets/offroad/icon_blank.png",
    },
    {
      "StandStillTimer",
      tr("Display Stand Still Timer"),
      tr("Enable this will display time spent at a stop (i.e., at a stop lights, stop signs, traffic congestions)."),
      "../assets/offroad/icon_blank.png",
    },
    {
      "ReverseDmCam",
      tr("Display DM Camera in Reverse Gear"),
      tr("Show Driver Monitoring camera while the car is in reverse gear."),
      "../assets/offroad/icon_blank.png",
    },
    {
      "ShowDebugUI",
      tr("OSM: Show debug UI elements"),
      tr("OSM: Show UI elements that aid debugging."),
      "../assets/offroad/icon_blank.png",
    },
    {
      "TrueVEgoUi",
      tr("Speedometer: Display True Speed"),
      tr("Display the true vehicle current speed from wheel speed sensors."),
      "../assets/offroad/icon_blank.png",
    },
    {
      "HideVEgoUi",
      tr("Speedometer: Hide from Onroad Screen"),
      tr("Hides the large current-speed display from the driving screen. Speed information in other UI areas is not affected."),
      "../assets/offroad/icon_blank.png",
    },
    {
      "EndToEndLongAlertUI",
      tr("Display End-to-end Longitudinal Status (Beta)"),
      tr("Enable this will display an icon that appears when the End-to-end model decides to start or stop."),
      "../assets/offroad/icon_blank.png",
    },
    {
      "MapboxFullScreen",
      tr("Navigation: Display in Full Screen"),
      QString(tr("Enable this will display the built-in navigation in full screen.<br>To switch back to driving view, <font color='yellow'>tap on the border edge</font>.")),
      "../assets/offroad/icon_blank.png",
    },
    {
      "Map3DBuildings",
      tr("Map: Display 3D Buildings"),
      tr("Parse and display 3D buildings on map. Thanks to jakethesnake420 for this implementation."),
      "../assets/offroad/icon_blank.png",
    },
  };

  // Visuals: Developer UI Info (Dev UI)
  std::vector<QString> dev_ui_settings_texts{tr("Off"), tr("5 Metrics"), tr("10 Metrics")};
  dev_ui_settings = new ButtonParamControl(
    "DevUIInfo", tr("Developer UI"), tr("Displays either 5 or 10 real-time diagnostic metrics on the driving screen. Select Off to hide them."),
    "../assets/offroad/icon_blank.png",
    dev_ui_settings_texts,
    380
  );
  dev_ui_settings->showDescription();

  // Visuals: Display Metrics above Chevron
  std::vector<QString> chevron_info_settings_texts{tr("Off"), tr("Distance"), tr("Speed")};
  chevron_info_settings = new ButtonParamControl(
    "ChevronInfo", tr("Metrics above Chevron"), tr("Displays distance or relative speed above the lead-vehicle chevron. This is available only when openpilot controls acceleration and braking."),
    "../assets/offroad/icon_blank.png",
    chevron_info_settings_texts,
    320
  );
  chevron_info_settings->showDescription();

  for (auto &[param, title, desc, icon] : toggle_defs) {
    auto toggle = new ParamControl(param, title, desc, icon, this);

    addItem(toggle);
    toggles[param.toStdString()] = toggle;

    if (param == "StandStillTimer") {
      addItem(dev_ui_settings);
    }

    if (param == "HideVEgoUi") {
      addItem(chevron_info_settings);
    }
  }

  std::vector<QString> sidebar_temp_texts{tr("Off"), tr("Ambient"), tr("RAM"), tr("CPU"), tr("GPU"), tr("Max")};
  sidebar_temp_setting = new ButtonParamControl(
    "SidebarTemperatureOptions", tr("Display Temperature on Sidebar"),
    tr("Selects which temperature appears in the driving-screen sidebar: ambient, memory, CPU, GPU, or the highest measured value. Select Off to hide it."),
    "../assets/offroad/icon_blank.png",
    sidebar_temp_texts,
    255
  );
  sidebar_temp_setting->showDescription();
  addItem(sidebar_temp_setting);

  // trigger offroadTransition when going onroad/offroad
  connect(uiState(), &UIState::offroadTransition, [=](bool offroad) {
  });

  QObject::connect(toggles["MapboxFullScreen"], &ToggleControl::toggleFlipped, [=](bool state) {
    toggles["MapboxFullScreen"]->showDescription();
  });
}
