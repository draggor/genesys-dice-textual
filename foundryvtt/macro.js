(() => {

class GenesysRoller {
  static async skillRoll({ actor, characteristic, skillId, formula, symbols, description }) {
    var _a2, _b;
    const roll = new Roll(formula, { symbols });
    await roll.evaluate({ async: true });
    const results = this.parseRollResults(roll);

    if (description) {

    } else if (skillId === "-") {
      if (characteristic) {
        description = game.i18n.format("Genesys.Rolls.Description.Characteristic", {
          characteristic: game.i18n.localize(`Genesys.Characteristics.${characteristic.capitalize()}`)
        });
      } else if (!actor) {
        description = game.i18n.localize("Genesys.Rolls.Description.Simple");
      }
    } else if (actor) {
      if (characteristic) {
        description = game.i18n.format("Genesys.Rolls.Description.Skill", {
          skill: ((_a2 = actor.items.get(skillId)) == null ? void 0 : _a2.name) ?? "UNKNOWN",
          characteristic: game.i18n.localize(`Genesys.CharacteristicAbbr.${characteristic.capitalize()}`)
        });
      } else {
        description = game.i18n.format("Genesys.Rolls.Description.SkillWithoutCharacteristic", {
          skill: ((_b = actor.items.get(skillId)) == null ? void 0 : _b.name) ?? "UNKNOWN"
        });
      }
    }
    const rollData = {
      description,
      results
    };
    const html = await renderTemplate("systems/genesys/templates/chat/rolls/skill.hbs", rollData);
    const chatData = {
      user: game.user.id,
      speaker: { actor: actor == null ? void 0 : actor.id },
      content: html,
      type: CONST.CHAT_MESSAGE_TYPES.ROLL,
      roll
    };
    await ChatMessage.create(chatData);
  }
  static async attackRoll({
    actor,
    characteristic,
    skillId,
    formula,
    symbols,
    weapon
  }) {
    var _a2, _b;
    const roll = new Roll(formula, { symbols });
    await roll.evaluate({ async: true });
    const results = this.parseRollResults(roll);
    let description = void 0;
    let totalDamage = weapon.systemData.baseDamage;
    let damageFormula = weapon.systemData.baseDamage.toString();
    const withDamageCharacteristic = weapon.systemData.damageCharacteristic;
    if (actor && withDamageCharacteristic && withDamageCharacteristic !== "-") {
      totalDamage += actor.system.characteristics[withDamageCharacteristic];
      damageFormula = game.i18n.localize(`Genesys.CharacteristicAbbr.${withDamageCharacteristic.capitalize()}`) + ` + ${damageFormula}`;
    }
    if (results.netSuccess > 0) {
      totalDamage += results.netSuccess;
    }
    if (skillId === "-") {
      if (characteristic) {
        description = game.i18n.format("Genesys.Rolls.Description.AttackCharacteristic", {
          name: weapon.name,
          characteristic: game.i18n.localize(`Genesys.Characteristics.${characteristic.capitalize()}`)
        });
      }
    } else if (actor) {
      if (characteristic) {
        description = game.i18n.format("Genesys.Rolls.Description.AttackSkill", {
          name: weapon.name,
          skill: ((_a2 = actor.items.get(skillId)) == null ? void 0 : _a2.name) ?? "UNKNOWN",
          characteristic: game.i18n.localize(`Genesys.CharacteristicAbbr.${characteristic.capitalize()}`)
        });
      } else {
        description = game.i18n.format("Genesys.Rolls.Description.AttackSkillWithoutCharacteristic", {
          name: weapon.name,
          skill: ((_b = actor.items.get(skillId)) == null ? void 0 : _b.name) ?? "UNKNOWN"
        });
      }
    }
    const attackQualities = weapon.systemData.qualities;
    await Promise.all(
      attackQualities.map(async (quality) => {
        quality.description = await TextEditor.enrichHTML(quality.description, { async: true });
      })
    );
    const rollData = {
      description,
      results,
      totalDamage,
      damageFormula,
      critical: weapon.systemData.critical,
      // tbh I can't be assed to implement another Handlebars helper for array length so let's just do undefined. <.<
      qualities: weapon.systemData.qualities.length === 0 ? void 0 : attackQualities,
      showDamageOnFailure: CONFIG.genesys.settings.showAttackDetailsOnFailure
    };
    const html = await renderTemplate("systems/genesys/templates/chat/rolls/attack.hbs", rollData);
    const chatData = {
      user: game.user.id,
      speaker: { actor: actor == null ? void 0 : actor.id },
      rollMode: game.settings.get("core", "rollMode"),
      content: html,
      type: CONST.CHAT_MESSAGE_TYPES.ROLL,
      roll
    };
    await ChatMessage.create(chatData);
  }
  static parseRollResults(roll) {
    const faces = roll.dice.reduce((faces2, die) => {
      const genDie = die;
      if (faces2[genDie.denomination] === void 0) {
        faces2[genDie.denomination] = die.results.map((r2) => genDie.getResultLabel(r2));
      } else {
        faces2[genDie.denomination].concat(die.results.map((r2) => genDie.getResultLabel(r2)));
      }
      return faces2;
    }, {});
    const results = Object.values(faces).flatMap((v2) => v2).flatMap((v2) => v2.split("")).filter((v2) => v2 !== " ").reduce(
      (results2, result) => {
        results2[result] += 1;
        return results2;
      },
      {
        a: 0,
        s: 0,
        t: 0,
        h: 0,
        f: 0,
        d: 0
      }
    );
    const extraSymbols = roll.data.symbols;
    if (extraSymbols) {
      for (const symbol of ["a", "s", "t", "h", "f", "d"]) {
        results[symbol] += extraSymbols[symbol] ?? 0;
      }
    }
    results["s"] += results["t"];
    results["f"] += results["d"];
    return {
      totalSuccess: results["s"],
      totalFailures: results["f"],
      totalAdvantage: results["a"],
      totalThreat: results["h"],
      totalTriumph: results["t"],
      totalDespair: results["d"],
      netSuccess: results["s"] - results["f"],
      netFailure: results["f"] - results["s"],
      netAdvantage: results["a"] - results["h"],
      netThreat: results["h"] - results["a"],
      faces,
      extraSymbols
    };
  }
}

function makeSpan(symbol, color) {
    return `<span style="font-family: 'Genesys Symbols', sans-serif; color: ${color}; -webkit-text-stroke: 1px black;">${symbol}</span>`;
}

const symbol_display = {
    "{P}": makeSpan('P', '#fff200'),
    "{A}": makeSpan('A', '#41ad49'),
    "{B}": makeSpan('B', '#72cddc'),
    "{C}": makeSpan('C', '#761213'),
    "{D}": makeSpan('D', '#522380'),
    "{S}": makeSpan('S', '#1e1e1e'),
}

function replaceSymbols(text, key) {
    return text.replaceAll(key, symbol_display[key]);
}

function main (scope) {
    let description = scope.description.replaceAll('|', ' ').replaceAll('\\n', '<br>');
    const title = scope.title?.replaceAll('|', ' ');
    if (title) {
        description = `<label>${title}</label><br>${description}<br>`;
    }

    description = Object.keys(symbol_display).reduce(replaceSymbols, description);

    const formula = scope.roll;

    GenesysRoller.skillRoll({token,actor,formula,description});
}

main(scope);

})();
