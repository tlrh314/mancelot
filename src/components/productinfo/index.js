import { h, Component } from 'preact';
import style from './style';

export default class Productinfo extends Component {

    static defaultProps = {
        color : "#FF0000"
    };

    render() {
        return (
          <div class="productinfo_container">
            <div class="icons_container">
              <div class="icon icon_vegan"></div>
              <div class="icon icon_fairtrade"></div>
              <div class="icon icon_environment"></div>
              <div class="icon icon_localproduced"></div>
              <div class="icon icon_localsupport"></div>
            </div>
            <div class="betterlives"></div>
            <div class="explain_brand">
              <p>
                Supermegaflex staat voor positiviteit, duurzaamheid en kwaliteit. Dit doet Supermegaflex door sweaters en t-shirts van hoge kwaliteit te verkopen met teksten die mensen blij maken. De sweaters en shirts van Supermegaflex zijn daarom eerlijk en milieuvriendelijk geproduceerd in Turkije. Ze dragen het GOTS-certificaat, een van de beste duurzame en eerlijke certificeringen die je kunt hebben. Daarnaast zijn de opdrukken Direct To Garment (DTG) geprint, wat betekent dat de verf op waterbasis en biologisch afbreekbaar is, maar ook jarenlang meegaat zonder kleur te verliezen.
              </p>
              <p>
                Supermegaflex heeft een ruime collectie aan sweaters en t-shirt met verschillende teksten en stijlen. Je kunt dus zelf je lievelingstrui of t-shirt kiezen met je eigen favoriete tekst, kleur en stijl. De sweaters en t-shirts zijn geschikt voor zowel mannen als vrouwen. "Tu es formidable", "Just smile!", "Dance like nobody is watching!" zijn een greep uit de positieve kreten.
              </p>
              <p>
                Er is goed onderzoek verricht naar het model van de sweaters en shirts, de kwaliteit van de stof en de bedrukking. Het resultaat: een lievelingstrui of t-shirt waar je een goed gevoel van krijgt, die heerlijk zit én jarenlang mee kan.
              </p>
            </div>
          </div>
        );
    }
}
