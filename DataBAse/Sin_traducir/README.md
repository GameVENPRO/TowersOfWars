Aquí se recoge parte de la información sobre el juego [Chat Wars] (https://telegram.me/ChatWarsBot?start=bb6bc6065e8648c0911c8776e277181d) utilizado como parte del bot de ayuda [Redwing] (https://t.me/RedwingBot).

Puedes seguir las noticias del bot en el canal: [Redwing News] (https://t.me/RedwingNews).

Si encuentra un error en los datos proporcionados, por favor [contacto] (https://t.me/motw_we) conmigo.

# resources.json
```json
{
    "id": 175,
    "name": "material de Embalaje",
    "aliases": ["material de Embalaje"],
    "cost": 1,
    "weight": 1,
    "recipeId": 145
}
```
* 'id` - número de recurso en el juego. Utilizado en comandos:
	* 🏰Bloqueo - > 🏚Tienda - > compra de recursos: ` / s_{id}`;
	* 🏰Bloqueo - > ⚒Taller - > ⚒banco de Trabajo: `/a_{id} ' `' / d_{id}`;
	* ` / inv` - > 🗃Otros `' / use_{id} ' ` para cofres);
	* [@ChatWarsTradeBot](https://t.me/ChatWarsTradeBot): `/add_{id - 1}`, `/del_{id - 1}`.
`'name` - el nombre del recurso tal como lo muestra [Redwing] (https://t.me/RedwingBot), en general un campo redundante, se pueden utilizar variantes de' aliases`;
* 'aliases' - una serie de nombres bajo los cuales el recurso se reunió / se encuentra en el juego;
* 'cost` - el precio del recurso cuando se vende en la tienda;
* 'weight' - espacio ocupado por el recurso en el almacén;
* 'recipeId' - número de receta, si el recurso se puede crear. De lo contrario, el campo no está presente.

# items.json
```json
{
    "id": 111,
    "name": "Guardián",
    aliases: [the Guardian, Doomsday Complex],
    "type": "spear",
    "cost": 5270,
    "weight": 180,
    "wrap": 2,
    "attributes": {
        "attack": 17,
        "defense": 15
    },
    "restrictions": {
        "level": 20,
        "defense": 10
    },
    "recipeId": 119
}
```
* 'id' - número de artículo en el juego. Utilizado en comandos:
	* /inv: `/on_{id}`, `/off_{id}`;
	* / inv: ` / use_{id} ' ` para pociones);
	* / inv -> 🏷Equipo: ` / bind_{id}`;
	* 🏰Castillo - > 🏚Tienda - >звер colección de animales - >зав Tener una mascota ` '/ getpet_{id} ' ` para cupones de animales);
	* 🏰Castillo - > 🏚Tienda - > comprar artículos: ` / sell_{id}`;
	* 🏰Bloqueo - > ⚒Taller - > 🏷Paquete `' / wrap_{id}`;
	* [@ChatWarsTradeBot](https://t.me/ChatWarsTradeBot): `/add_{id + 1100}`, `/del_{id + 1100}`;
`'name' - el nombre del objeto, en general un campo redundante, puede utilizar variantes de ' aliases`;
* 'aliases' - una serie de nombres bajo los cuales el objeto se encuentra / se encuentra en el juego. Los nuevos nombres están relacionados con [los inocentes эвентом](https://wiki.chatwars.me/%D0%97%D0%B2%D0%B5%D0%B7%D0%B4%D0%BD%D1%8B%D0%B5_%D0%B2%D0%BE%D0%B9%D0%BD%D1%8B);
* 'type' - el tipo de objeto, ahora no siempre es preciso y requiere la alteración de las ranuras reales disponibles para las cosas del personaje;
`'cost' - el precio del artículo cuando se compra en la tienda. Cuando se vende de nuevo, el costo es igual a ' floor (0.3 * cost)`. Para los artículos que no se pueden comprar en la tienda, el precio se establece para que el valor de venta calculado coincida con el valor del juego;
`'peso' - el espacio ocupado por un artículo en el almacén. Para el equipo, se indica el valor en estado envuelto (las cosas en la mochila no ocupan espacio en el almacén). '0.1' es un indicador de que el valor es desconocido en este momento;
* 'wrap`: cantidad de material de embalaje necesario para empacar un artículo con ` / wrap_{id}`;
`'atributos' - características del sujeto (⚔️|🛡|🍀|🔋|⛏);
* 'restricciones' - requisitos necesarios para poner un artículo. La información sobre ellos probablemente no esté completa;
`'commands`: comandos relacionados con un objeto, pero que no utilizan su`id'. Por el momento, solo está comprando artículos en la tienda;
* 'recipeId': el número de la receta correspondiente si el artículo es artesanal.

# recipes.json
```json
{
    "recipeId": 130,
    "name": "Tridente",
    "type": "item",
    "tier": 4,
    "ingredients": [
        { "id": 102, "count": 1200 },
        { "id": 117, "count": 5 },
        { "id": 123, "count": 23 },
        { "id": 126, "count": 23 },
        { "id": 139, "count": 5 },
        { "id": 144, "count": 1 },
        { "id": 145, "count": 1 },
        { "id": 146, "count": 14 }
    ],
    "status": "confirmed"
}
```
* 'recipeId' - número de receta. Se utiliza en el comando '/ craft_{recipeId} ' ` Замок Castillo - > маст Taller - > Рецепты recetas);
`'nombre': el nombre del objeto o recurso que se está fabricando;
* `type` - `(resource|item)`;
* 'nivel': el nivel de habilidad 'Artesanal' requerido para usar una receta. Por el momento, no se ha verificado la información, ¿Cuál es la diferencia entre el primer nivel de artesanía y la falta de habilidad como tal;
* 'ingredientes' - una serie de ingredientes que forman parte del recurso. 'id' es el número de recurso ` 'count' es su número;
`'status' - estado de la receta:
	`'incomplete' - la receta no está abierta hasta el final;
	* ` complete ' - la receta está abierta en su totalidad, pero nadie lo ha hecho todavía;
	* ` confirmed ' - la receta se ha utilizado con éxito.