import random
from app.model import Personaje

def aplicar_modificadores_raza(personaje):
    
    stats = {
        "nombre": personaje.nombre,
        "raza": personaje.raza,
        "fuerza": personaje.fuerza or 0,
        "agilidad": personaje.agilidad or 0,
        "magia": personaje.magia or 0,
        "conocimiento": personaje.conocimiento or 0
    }

    raza = str(stats["raza"]).strip().lower()

    if raza == 'humano':
        stats["fuerza"] += 5
        stats["agilidad"] += 5
        stats["magia"] += 5
        stats["conocimiento"] += 5
    elif raza == 'elfo':
        stats["fuerza"] -= 5
        stats["agilidad"] += 15
        stats["magia"] += 15
        stats["conocimiento"] += 5
    elif raza == 'orco':
        stats["fuerza"] += 20
        stats["agilidad"] -= 5
        stats["magia"] -= 10
        stats["conocimiento"] -= 10
    elif raza == 'enano':
        stats["fuerza"] += 15
        stats["agilidad"] -= 10
        stats["magia"] -= 5
        stats["conocimiento"] += 10
        
    # Asegurar que las estadísticas no bajen de 1
    for stat in ["fuerza", "agilidad", "magia", "conocimiento"]:
        stats[stat] = max(1, stats[stat])
    
    return stats

def calcular_poder_batalla(stats):
    """
    Calcula el poder total aplicando pesos a cada estadística + Factor rándom.
    """
    # Puedes ajustar los pesos como prefieras
    poder_base = (stats["fuerza"] * 1.5) + (stats["agilidad"] * 1.2) + (stats["magia"] * 1.3) + (stats["conocimiento"] * 1.0)
    suerte = random.randint(1, 20) # Como en un clásico juego de rol (un dado D20)
    return poder_base + suerte, suerte

def simular_combate(personaje1, personaje2):
    if personaje1.id == personaje2.id:
        return {"error": "Un personaje no puede combatir consigo mismo."}

    # 1. Aplicamos los modificadores
    stats1 = aplicar_modificadores_raza(personaje1)
    stats2 = aplicar_modificadores_raza(personaje2)

    # 2. Calculamos el poder total en este turno
    poder1, suerte1 = calcular_poder_batalla(stats1)
    poder2, suerte2 = calcular_poder_batalla(stats2)

    # 3. Reporte de batalla
    log = []
    log.append(f"COMBATE: {stats1['nombre']} ({stats1['raza']}) VS {stats2['nombre']} ({stats2['raza']})")
    
    log.append(f"{stats1['nombre']} entra con -> F:{stats1['fuerza']} | A:{stats1['agilidad']} | M:{stats1['magia']} | C:{stats1['conocimiento']}")
    log.append(f"{stats2['nombre']} entra con -> F:{stats2['fuerza']} | A:{stats2['agilidad']} | M:{stats2['magia']} | C:{stats2['conocimiento']}")
    
    log.append(f"{stats1['nombre']} tira el dado de la suerte y saca un: {suerte1} (Poder total: {poder1:.1f})")
    log.append(f"{stats2['nombre']} tira el dado de la suerte y saca un: {suerte2} (Poder total: {poder2:.1f})")

    # 4. Determinamos Ganador
    if poder1 > poder2:
        ganador = stats1['nombre']
        log.append(f"¡{ganador} se alza con la victoria!")
    elif poder2 > poder1:
        ganador = stats2['nombre']
        log.append(f"¡{ganador} se alza con la victoria!")
    else:
        ganador = "Empate"
        log.append("¡El combate ha terminado en un empate legendario!")

    return {
        "ganador": ganador,
        "poder1": poder1,
        "poder2": poder2,
        "log": log
    }